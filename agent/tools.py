from services.graph import run_graph
from services.agent_llm_service import chat_answer
from services.environment_service import get_document_metadata



def rag_tool(query: str, **kwargs):

    result = run_graph(query)

    return result



def chat_tool(question : str,**kwargs) :

    return {
        "answer" : chat_answer(question),
        "chunks" : []
    }




def metadata_tool(**kwargs):

    metadata = get_document_metadata()

    return {
        "answer" : (
            f"Filename : {metadata['filename']}\n"
            f"Page count: {metadata['page_count']}\n"
            f"Chunk count: {metadata['chunk_count']}"
        ),
        "chunks" : []
    }



def citation_tool(query : str,**kwargs):

    result = run_graph(query)

    citations = []

    for chunk in result["chunks"]:

        citations.append({
            "page" : chunk["page"],
            "text" : chunk["text"]
        })

    return {
        "answer" : "Relevant sources retrieved.",
        "chunks" : citations
    }

def summarize_tool(query : str ,**kwargs):

    result = run_graph(query)

    chunks = result["chunks"]

    if not chunks:
        return {
            "answer": "No relevant content found.",
            "chunks": []
        }

    context = "\n\n".join(
        chunk["text"]
        for chunk in chunks
    )

    prompt = f"""Summarize the following content clearly and concisely.
    content : 
    {context}
    """
    answer = chat_answer(prompt)

    return {
        "answer" : answer,
        "chunks" : []
    }

TOOLS = {
    "rag": rag_tool,
    "chat": chat_tool,
    "metadata" : metadata_tool,
    "citation" : citation_tool,
    "summarize" : summarize_tool
}