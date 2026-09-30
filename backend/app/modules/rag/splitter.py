from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(docs):
    
  
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", ".", " "]  
    )

    chunks = splitter.split_documents(docs)
    return chunks