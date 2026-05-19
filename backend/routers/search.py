from fastapi import APIRouter, HTTPException
from backend.models.schemas import SearchRequest, SearchResponse
from backend.services.gemma_service import GemmaService

router = APIRouter()
gemma = GemmaService()

@router.post("/", response_model=SearchResponse)
def search_emails(req: SearchRequest):
    try:
        answer = gemma.search(req.emails, req.question)
        return SearchResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))