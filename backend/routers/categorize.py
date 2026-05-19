from fastapi import APIRouter, HTTPException
from backend.models.schemas import CategorizeRequest, CategorizeResponse
from backend.services.gemma_service import GemmaService

router = APIRouter()
gemma = GemmaService()

@router.post("/", response_model=CategorizeResponse)
def categorize_email(req: CategorizeRequest):
    try:
        category = gemma.categorize(req.email_body)
        return CategorizeResponse(category=category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))