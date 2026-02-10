from fastapi import APIRouter, HTTPException
from typing import List
from schemas import Document, SearchQuery, SearchResult
from service import search_service

router = APIRouter()

@router.post("/ingest")
async def ingest_documents(documents: List[Document]):
    try:
        count = search_service.upload_documents(documents)
        return {"message": f"Successfully indexed {count} documents"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search", response_model=List[SearchResult])
async def search(query: SearchQuery):
    try:
        results = search_service.search(
            query=query.query,
            limit=query.limit,
            filter_key=query.filter_key,
            filter_value=query.filter_value
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))