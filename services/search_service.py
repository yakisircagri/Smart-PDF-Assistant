from elasticsearch import Elasticsearch
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from langfuse import observe



es = Elasticsearch("http://localhost:9200")


@observe(name = "semantic_search_method")
def semantic_search(query : str):

    embeddings = OpenAIEmbeddings(
        model = "text-embedding-3-small"
    )

    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )

    results = vectorstore.similarity_search(
        query,
        k = 5
    )

    return  [
        {
            "text": doc.page_content,
            "page": doc.metadata.get("page")
        }
        for doc in results
    ]


@observe(name = "keyword_search_method")
def keyword_search(query : str):

    response = es.search(
        index = "documents",
        query = {
            "match" : {
                "content" : query
            }
        }
    )

    return [
    {
        "text": hit["_source"]["content"],
        "page": hit["_source"]["metadata"]
    }
    for hit in response["hits"]["hits"]
]

@observe(name = "hybrid_search_method")
def hybrid_search(query : str):

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )

    semantic_results = vectorstore.similarity_search_with_score(
        query,
        k = 5
    )
    keyword_results = es.search(
        index = "documents",
        query = {
            "match" : {
                "content" : query
            }
        }
    )
    scores = {}
    k = 60
    for rank, (doc,score) in enumerate(semantic_results):

        key = doc.page_content

        if key not in scores:
            scores[key] = {
                "score": 0,
                "metadata": doc.metadata
            }
        scores[key]["score"] += 1 / (k + rank + 1)

    for rank , hit in enumerate(keyword_results["hits"]["hits"]):

        key = hit["_source"]["content"]

        if key not in scores:
            scores[key] = {
                "score": 0,
                "metadata": {
                    "page": hit["_source"]["metadata"],
                    "source": hit["_source"]["source"]
                }
            }
        scores[key]["score"] += 1 / (k + rank + 1)

    final_results = sorted(
        scores.items(),
        key = lambda x: x[1]["score"],
        reverse = True
    )

    return [
    {
        "text": content,
        "page": data["metadata"]
    }
    for content, data in final_results[:5]
]