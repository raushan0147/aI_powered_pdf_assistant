from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    Filter,
    FieldCondition,
    MatchValue,
    PayloadSchemaType,
)
from langchain_qdrant import QdrantVectorStore

from app.core.config import settings


embeddingModel = HuggingFaceEmbeddings(
    model_name=settings.HUGGINGFACE_EMBEDDING_MODEL
)

client = QdrantClient(
    url=settings.QDRANT_ENDPOINT,
    api_key=settings.QDRANT_API_KEY,
    timeout=60
)


def create_collection_if_not_exists():
    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if settings.QDRANT_COLLECTION not in names:
        client.create_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

    # Required for filtering/deleting by user_id in Qdrant Cloud
    try:
        client.create_payload_index(
            collection_name=settings.QDRANT_COLLECTION,
            field_name="metadata.user_id",
            field_schema=PayloadSchemaType.INTEGER
        )
    except Exception:
        pass


def get_vector_store():
    create_collection_if_not_exists()

    return QdrantVectorStore(
        client=client,
        collection_name=settings.QDRANT_COLLECTION,
        embedding=embeddingModel
    )


def delete_user_embeddings(user_id: int):
    create_collection_if_not_exists()

    client.delete(
        collection_name=settings.QDRANT_COLLECTION,
        points_selector=Filter(
            must=[
                FieldCondition(
                    key="metadata.user_id",
                    match=MatchValue(value=int(user_id))
                )
            ]
        )
    )


def store_documents(splitted_docs, user_id: int, filename: str):
    create_collection_if_not_exists()

    # Delete only this user's old embeddings
    delete_user_embeddings(user_id)

    # Add user metadata to every chunk
    for doc in splitted_docs:
        doc.metadata["user_id"] = int(user_id)
        doc.metadata["filename"] = filename

    vector_store = get_vector_store()

    vector_store.add_documents(splitted_docs)

    return {
        "message": "PDF embedding stored successfully",
        "user_id": user_id,
        "filename": filename,
        "total_chunks": len(splitted_docs)
    }


def search_user_documents(query: str, user_id: int, k: int = 3):
    vector_store = get_vector_store()

    results = vector_store.similarity_search(
        query=query,
        k=k,
        filter=Filter(
            must=[
                FieldCondition(
                    key="metadata.user_id",
                    match=MatchValue(value=int(user_id))
                )
            ]
        )
    )

    return results