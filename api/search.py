from fastapi import APIRouter, HTTPException

from models.schemas import SearchRequest

from services.graph import graph


router=APIRouter()


@router.post("/search")
def search(request:SearchRequest):

    result = graph.invoke(
        {
            "query":request.query,
        }

    )

    return {
        "answer":result["answer"],
        "chunks":result["chunks"],
    }