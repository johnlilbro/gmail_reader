# gmail_reader

A read-only Gmail integration for `johnlilbro1977@gmail.com`.

## Purpose

This repo is for safe read-only Gmail access so lilbro can:
- authenticate with Gmail API
- read inbox contents
- inspect unread messages
- later summarize important mail

## Scope

The app uses the Gmail read-only scope:

```text
https://www.googleapis.com/auth/gmail.readonly
```

## Files

- `client_secret.json` — OAuth client credentials (not committed)
- `token.json` — generated after first successful auth (not committed)
- `gmail_reader.py` — main script

## Setup

```bash
uv venv
uv pip install -r requirements.txt
```

## First auth

```bash
.venv/bin/python gmail_reader.py auth
```

For the easiest setup, run the auth flow on a laptop or desktop with a browser. That will create `token.json`, which you can then copy to the server for read-only use.

## Check unread mail

```bash
.venv/bin/python gmail_reader.py unread
```
