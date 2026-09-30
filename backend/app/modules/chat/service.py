from functools import lru_cache
from typing import Literal

from pydantic import BaseModel, Field

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import (
    RunnableLambda,
    RunnableBranch,
    RunnablePassthrough,
    RunnableParallel,
)
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

from app.core.config import settings
from app.modules.rag.vectorstore import search_user_documents


class QuestionInfo(BaseModel):
    info: Literal["greet", "identity", "other"] = Field(
        description="Classification of user question"
    )


classification_parser = PydanticOutputParser(pydantic_object=QuestionInfo)


@lru_cache(maxsize=1)
def get_llm_model():
    llm = HuggingFaceEndpoint(
        repo_id=settings.HUGGINGFACE_LLM_MODEL,
        task="text-generation",
        temperature=0.1,
    )
    return ChatHuggingFace(llm=llm)


def create_classification_prompt():
    return PromptTemplate(
        template="""
You are a strict question classifier.

Classify the user question into exactly ONE category.

Categories:

1. greet
Use this when the user is greeting or starting conversation.
Examples:
- hi
- hello
- hey
- hey bro
- good morning
- good evening
- how are you

2. identity
Use this when the user asks about their identity or logged-in user information.
Examples:
- who am I
- do you know me
- what is my name
- tell me about me
- do you know my name

3. other
Use this for everything else.
Examples:
- what is pharmacokinetics
- explain this PDF
- tell me a joke
- what is AI

Important Rules:
1. Return ONLY valid JSON.
2. Do NOT explain.
3. Do NOT add markdown.
4. The value of "info" must be only one of:
   "greet", "identity", "other"

Question:
{question}

{format_instructions}
""",
        input_variables=["question"],
        partial_variables={
            "format_instructions": classification_parser.get_format_instructions()
        },
    )


def create_user_answer_prompt():
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are a friendly assistant for a logged-in user.

User Info:
User ID: {user_id}
User Name: {user_name}

Rules:
1. If classification is greet:
   - Greet the user politely.
   - Use the user's name.
   - Ask how you can help with their PDF.
   - Keep it friendly and natural.

2. If classification is identity:
   - Answer using ONLY the given User Info.
   - Mention the user's name.
   - Mention the user ID only if it is helpful.
   - Explain that you know me because you are user of this platform.
   - Do not say anything that is not present in User Info.

3. Do not use PDF context here.
4. Do not use outside knowledge.
5. Keep the answer descriptive but not too long.
""",
            ),
            (
                "human",
                """
Classification: {info}
User Question: {question}

Answer:
""",
            ),
        ]
    )


def retrieve_docs_from_qdrant(question: str, user_id: int):
    return search_user_documents(
        query=question,
        user_id=user_id,
        k=8,
    )


def make_context(docs):
    context = ""

    for index, doc in enumerate(docs, start=1):
        context += f"""
Chunk {index}
Filename: {doc.metadata.get("filename")}
Page: {doc.metadata.get("page_label") or doc.metadata.get("page")}
User: {doc.metadata.get("user_id")}

Content:
{doc.page_content}

"""
    return context.strip()


def create_pdf_prompt():
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are a PDF assistant.

Rules:
1. Answer only from the given PDF context.
2. Use page number if helpful.
3. If answer is not found, say exactly:
"Sorry to say that this question not belongs to this pdf"
4. Do not use outside knowledge.
5. Do not guess.
""",
            ),
            (
                "human",
                """
PDF Context:
{context}

User Question:
{question}

Answer:
""",
            ),
        ]
    )


def create_pdf_rag_chain():
    prompt = create_pdf_prompt()
    model = get_llm_model()
    parser = StrOutputParser()

    chain = RunnablePassthrough.assign(
        docs=RunnableLambda(
            lambda x: retrieve_docs_from_qdrant(
                question=x["question"],
                user_id=x["user_id"],
            )
        )
    ) | RunnableBranch(
        (
            lambda x: len(x["docs"]) > 0,
            RunnablePassthrough.assign(
                context=RunnableLambda(lambda x: make_context(x["docs"]))
            )
            | RunnableParallel(
                context=RunnableLambda(lambda x: x["context"]),
                question=RunnableLambda(lambda x: x["question"]),
            )
            | prompt
            | model
            | parser,
        ),
        RunnableLambda(lambda x: "Answer not found in the PDF."),
    )

    return chain


def ask_question_service(question: str, user):
    llm = get_llm_model()

    classifier_chain = create_classification_prompt() | llm | classification_parser

    user_answer_chain = create_user_answer_prompt() | llm | StrOutputParser()

    pdf_rag_chain = create_pdf_rag_chain()

    full_chain = RunnableLambda(
        lambda x: {
            "classification": classifier_chain.invoke({"question": x["question"]}),
            "question": x["question"],
            "user_id": x["user"].id,
            "user_name": x["user"].name,
        }
    ) | RunnableBranch(
        (
            lambda x: x["classification"].info in ["greet", "identity"],
            RunnableLambda(
                lambda x: {
                    "info": x["classification"].info,
                    "question": x["question"],
                    "user_id": x["user_id"],
                    "user_name": x["user_name"],
                }
            )
            | user_answer_chain,
        ),
        RunnableLambda(
            lambda x: {
                "question": x["question"],
                "user_id": x["user_id"],
            }
        )
        | pdf_rag_chain,
    )

    result = full_chain.invoke(
        {
            "question": question,
            "user": user,
        }
    )

    return {
        "question": question,
        "answer": result,
    }
