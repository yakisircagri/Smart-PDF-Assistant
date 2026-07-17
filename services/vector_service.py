from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma


embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)


vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)