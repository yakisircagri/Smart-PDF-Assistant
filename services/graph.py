from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from services.router import route_query

from services.search_service import (
    semantic_search,
    hybrid_search,
    keyword_search
)

from langfuse import observe

from services.llm_service import generate_answer

from services.langfuse_service import langfuse



class GraphState(TypedDict):
    query : str
    chunks : list
    answer : str
    messages : list


def router(state):

    return state



def route(state):

    with langfuse.start_as_current_observation(
        name = "Router" ,
        as_type = "chain"
    ) as span :

        decision = route_query(state["query"])

        span.update(
            input={
                "query": state["query"]
            },
            output={
                "route": decision
            }
        )
        return decision




def semantic_node(state):
    with langfuse.start_as_current_observation(
        name = "Semantic Search Method" ,
        as_type = "retriever"
    ) as span :

        state["chunks"] = semantic_search(state["query"])

        span.update(
            output = {
                "Number of chunks" : len(state["chunks"])
            }
        )

        return state



def hybrid_node(state):
    with langfuse.start_as_current_observation(
        name = "Hybrid Search" ,
        as_type = "retriever"
    ) as span :

        state["chunks"] = hybrid_search(state["query"])

        span.update(
            output = {
                "retrieved_chunks" : len(state["chunks"])
            }
        )

        return state



def keyword_node(state):

    with langfuse.start_as_current_observation(
        name = "Keyword Search" ,
        as_type = "retriever"
    ) as span :

        state["chunks"] = keyword_search(state["query"])

        span.update(
            output = {
                "retrieved_chunks" : len(state["chunks"])
            }
        )

        return state



def generate(state):

    with langfuse.start_as_current_observation(
        name = "Generate" ,
        as_type = "generation"
    ) as span :

        state["answer"] = generate_answer(
            state["query"],
            state["chunks"],
        )

        span.update(
            input = {
                "query": state["query"],
                "chunk_count" : len(state["chunks"])
            },

            output = {
                "answer_lenght" : len(state["answer"]),
            }
        )

        return state



builder = StateGraph(GraphState)

builder.add_node("router",router)
builder.add_node("semantic",semantic_node)
builder.add_node("hybrid",hybrid_node)
builder.add_node("keyword",keyword_node)
builder.add_node("generate",generate)

builder.add_edge(START,"router")

builder.add_conditional_edges(
    "router" ,
    route ,
    {
        "semantic": "semantic",
        "keyword": "keyword",
        "hybrid": "hybrid"
    }
)

builder.add_edge("semantic","generate")
builder.add_edge("hybrid","generate")
builder.add_edge("keyword","generate")
builder.add_edge("generate", END)

graph = builder.compile()


@observe(name = "RAG Pipeline")
def run_graph(query : str):
    result = graph.invoke(
        {
            "query" : query,
            "chunks" : [],
            "answer" :"",
            "messages" : [],
        },

    )
    return result