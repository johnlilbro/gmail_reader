from __future__ import annotations

import base64
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

BASE_DIR = Path(__file__).resolve().parent
CLIENT_SECRET_FILE = BASE_DIR / "client_secret.json"
TOKEN_FILE = BASE_DIR / "token.json"
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_credentials() -> Credentials:
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        TOKEN_FILE.write_text(creds.to_json())
        return creds
    if creds and creds.valid:
        return creds

    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET_FILE), SCOPES)
    auth_url, _ = flow.authorization_url(prompt="consent")
    print("Open this URL in your browser and authorize access:\n")
    print(auth_url)
    print("\nPaste the full authorization code here:")
    code = input().strip()
    flow.fetch_token(code=code)
    creds = flow.credentials
    TOKEN_FILE.write_text(creds.to_json())
    return creds


def get_service():
    creds = get_credentials()
    return build("gmail", "v1", credentials=creds)


def auth_only():
    get_service()
    print("Authentication complete. token.json created.")


def unread_messages(limit: int = 10):
    service = get_service()
    results = service.users().messages().list(userId="me", labelIds=["UNREAD"], maxResults=limit).execute()
    messages = results.get("messages", [])
    if not messages:
        print("No unread messages.")
        return

    for msg in messages:
        detail = service.users().messages().get(userId="me", id=msg["id"], format="metadata", metadataHeaders=["From", "Subject", "Date"]).execute()
        headers = {h["name"]: h["value"] for h in detail.get("payload", {}).get("headers", [])}
        print("---")
        print("From:", headers.get("From", ""))
        print("Subject:", headers.get("Subject", ""))
        print("Date:", headers.get("Date", ""))
        print("ID:", msg["id"])


def main():
    if len(sys.argv) < 2:
        print("Usage: gmail_reader.py [auth|unread]")
        raise SystemExit(1)

    command = sys.argv[1]
    if command == "auth":
        auth_only()
    elif command == "unread":
        unread_messages()
    else:
        print(f"Unknown command: {command}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
