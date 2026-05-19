from fastapi import APIRouter, HTTPException
from backend.models.schemas import SummarizeRequest, SummarizeResponse
from backend.services.gemma_service import GemmaService

router = APIRouter()
gemma = GemmaService()

@router.post("/", response_model=SummarizeResponse)
def summarize_email(req: SummarizeRequest):
    try:
        summary = gemma.summarize(req.email_body)
        return SummarizeResponse(summary=summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))