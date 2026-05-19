import base64
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from backend.utils.logger import get_logger
from backend.models.schemas import Email

logger = get_logger(__name__)
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

class GmailService:
    def __init__(self):
        self.service = self._authenticate()

    def _authenticate(self):
        creds = None

        # Only load token.json if it exists AND is not empty
        if os.path.exists("token.json") and os.path.getsize("token.json") > 0:
            try:
                creds = Credentials.from_authorized_user_file("token.json", SCOPES)
            except Exception as e:
                logger.warning(f"token.json is corrupted, re-authenticating: {e}")
                creds = None

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open("token.json", "w", encoding="utf-8") as f:
                f.write(creds.to_json())

        logger.info("Gmail authenticated successfully")
        return build("gmail", "v1", credentials=creds)

    def fetch_emails(self, max_results: int = 20) -> list[Email]:
        results = self.service.users().messages().list(
            userId="me", maxResults=max_results
        ).execute()

        emails = []
        for msg in results.get("messages", []):
            try:
                message = self.service.users().messages().get(
                    userId="me", id=msg["id"], format="full"
                ).execute()
                email = self._parse_message(message)
                if email:
                    emails.append(email)
            except Exception as e:
                logger.error(f"Failed to parse email {msg['id']}: {e}")

        return emails

    def _parse_message(self, message: dict) -> Email | None:
        payload = message.get("payload", {})
        headers = {h["name"]: h["value"] for h in payload.get("headers", [])}

        body = ""
        if "data" in payload.get("body", {}):
            body = base64.urlsafe_b64decode(
                payload["body"]["data"]
            ).decode("utf-8", errors="ignore")
        elif "parts" in payload:
            for part in payload["parts"]:
                if part.get("mimeType") == "text/plain":
                    data = part.get("body", {}).get("data", "")
                    if data:
                        body = base64.urlsafe_b64decode(data).decode(
                            "utf-8", errors="ignore"
                        )
                        break

        if not body:
            return None

        return Email(
            id=message["id"],
            subject=headers.get("Subject", "(no subject)"),
            sender=headers.get("From", "unknown"),
            body=body[:3000],
            date=headers.get("Date", ""),
        )