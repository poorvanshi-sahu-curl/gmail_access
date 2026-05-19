from backend.services.gmail_service import GmailService

print("🔐 Starting Gmail authentication...")
print("   A browser window will open — log in and allow access.")
service = GmailService()
print("✅ Authentication successful! token.json saved.")
print("   You can now run the app normally.")