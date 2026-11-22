"""Contact form back end for the portfolio site (stretch goal 2).

Accepts a JSON POST with name, email and message, checks it, and saves it to
DynamoDB. Read your messages in the DynamoDB console under "Explore items".

Setup (see README.md in this folder):
  - DynamoDB table: name "contact-messages", partition key "id" (String)
  - Lambda runtime: Python 3.13, environment variable TABLE_NAME=contact-messages
  - Lambda role needs dynamodb:PutItem on the table
  - Function URL: auth type NONE, CORS allowing your Amplify site, method POST,
    header content-type
"""

import base64
import json
import os
import re
import uuid
from datetime import datetime, timezone

import boto3

TABLE_NAME = os.environ.get("TABLE_NAME", "contact-messages")
table = boto3.resource("dynamodb").Table(TABLE_NAME)

MAX_LENGTH = {"name": 100, "email": 200, "message": 2000}
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method", "")
    if method != "POST":
        return response(405, {"error": "Use POST"})

    raw = event.get("body") or ""
    if event.get("isBase64Encoded"):
        raw = base64.b64decode(raw).decode("utf-8", errors="replace")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return response(400, {"error": "Body must be JSON"})
    if not isinstance(data, dict):
        return response(400, {"error": "Body must be a JSON object"})

    # Spam trap: the hidden "website" field is only filled in by bots.
    # Pretend it worked so the bot moves on, but save nothing.
    if str(data.get("website", "")).strip():
        return response(200, {"ok": True})

    fields = {}
    for name, limit in MAX_LENGTH.items():
        value = data.get(name)
        if not isinstance(value, str) or not value.strip():
            return response(400, {"error": f"'{name}' is required"})
        value = value.strip()
        if len(value) > limit:
            return response(400, {"error": f"'{name}' must be {limit} characters or fewer"})
        fields[name] = value

    if not EMAIL_PATTERN.match(fields["email"]):
        return response(400, {"error": "'email' doesn't look like an email address"})

    table.put_item(
        Item={
            "id": str(uuid.uuid4()),
            "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            **fields,
        }
    )
    return response(200, {"ok": True})
