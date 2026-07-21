import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from services.elastic_service import es

from services.environment_service import set_document_count,set_document_metadata


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)



async def upload_pdf(file):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    loader = PyPDFLoader(file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 200,
        chunk_overlap = 100
    )

    chunks = text_splitter.split_documents(documents)

    if not es.indices.exists(index = "documents"):
        es.indices.create(index = "documents")

    for i,chunk in enumerate(chunks):
        es.index(
            index = "documents",
            id = f"{file.filename}_{i}",
            document =
            {
                "content" : chunk.page_content,
                "metadata": chunk.metadata.get("page"),
                "source" : file.filename
            }
        )

    set_document_count(len(chunks))

    set_document_metadata(
        filename=file.filename,
        page_count=len(documents),
        chunk_count=len(chunks),
    )

    embeddings = OpenAIEmbeddings(
        model = "text-embedding-3-small"
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )

    return {
        "page_count": len(documents),
        "chunk_count": len(chunks),
        "first_chunk": chunks[0].page_content
    }
