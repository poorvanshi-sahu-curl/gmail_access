from fastapi import APIRouter, HTTPException
from backend.models.schemas import DraftRequest, DraftResponse
from backend.services.gemma_service import GemmaService

router = APIRouter()
gemma = GemmaService()

@router.post("/", response_model=DraftResponse)
def draft_reply(req: DraftRequest):
    try:
        draft = gemma.draft_reply(req.email_body, req.tone)
        return DraftResponse(draft=draft)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))