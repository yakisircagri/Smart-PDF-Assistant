from fastapi import APIRouter, HTTPException

from models.schemas import SearchRequest

from agent.agent import ReactAgent


router=APIRouter()

agent = ReactAgent()


@router.post("/search")
def search(request:SearchRequest):

    result = agent.invoke(request.query)

    return {
        "answer":result["answer"],
        "chunks":result["chunks"],
        "tool" : result["tool"]
    }