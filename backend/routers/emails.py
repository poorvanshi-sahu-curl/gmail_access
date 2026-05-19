from fastapi import APIRouter, HTTPException
from backend.services.gmail_service import GmailService
from backend.config import settings

router = APIRouter()
gmail = GmailService()

@router.get("/")
def get_emails():
    try:
        emails = gmail.fetch_emails(max_results=settings.max_emails)
        return [e.dict() for e in emails]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))