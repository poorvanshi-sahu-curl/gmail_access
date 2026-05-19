from fastapi import FastAPI
from backend.routers import emails, summarize, draft, search, categorize

app = FastAPI(title="Gemma Gmail App", version="1.0.0")

app.include_router(emails.router,    prefix="/emails",    tags=["emails"])
app.include_router(summarize.router, prefix="/summarize", tags=["summarize"])
app.include_router(draft.router,     prefix="/draft",     tags=["draft"])
app.include_router(search.router,    prefix="/search",    tags=["search"])
app.include_router(categorize.router,prefix="/categorize",tags=["categorize"])

@app.get("/health")
def health():
    return {"status": "ok"}