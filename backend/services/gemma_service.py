import ollama
from backend.config import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)

class GemmaService:
    def __init__(self):
        self.model = settings.gemma_model

    def _chat(self, prompt: str) -> str:
        logger.info(f"Sending prompt to {self.model}")
        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]

    def summarize(self, email_body: str) -> str:
        prompt = f"""Summarize this email in 3 bullet points.
Be concise. Start each bullet with '•'.

Email:
{email_body}"""
        return self._chat(prompt)

    def draft_reply(self, email_body: str, tone: str = "professional") -> str:
        prompt = f"""Draft a {tone} email reply.
Be concise. Only return the reply body, no subject line.

Original email:
{email_body}"""
        return self._chat(prompt)

    def search(self, emails: list[str], question: str) -> str:
        context = "\n---\n".join(emails[:10])
        prompt = f"""You are an email assistant.
Answer this question based on the emails below.
If the answer is not in the emails, say "Not found in emails."

Question: {question}

Emails:
{context}"""
        return self._chat(prompt)

    def categorize(self, email_body: str) -> str:
        prompt = f"""Categorize this email into exactly ONE of:
[Work, Personal, Finance, Shopping, Newsletter, Spam, Urgent]

Reply with ONLY the category name, nothing else.

Email:
{email_body}"""
        return self._chat(prompt).strip()