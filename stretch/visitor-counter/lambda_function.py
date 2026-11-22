"""Visitor counter for the portfolio site (stretch goal 1).

Each call adds 1 to a counter stored in DynamoDB and returns the new total.

Setup (see README.md in this folder):
  - DynamoDB table: name "visitor-count", partition key "id" (String)
  - Lambda runtime: Python 3.13, environment variable TABLE_NAME=visitor-count
  - Lambda role needs dynamodb:UpdateItem on the table
  - Function URL: auth type NONE, CORS allowing your Amplify site
"""

import json
import os

import boto3

TABLE_NAME = os.environ.get("TABLE_NAME", "visitor-count")
table = boto3.resource("dynamodb").Table(TABLE_NAME)


def lambda_handler(event, context):
    # ADD creates the item and the attribute the first time, then increments.
    result = table.update_item(
        Key={"id": "site"},
        UpdateExpression="ADD visits :one",
        ExpressionAttributeValues={":one": 1},
        ReturnValues="UPDATED_NEW",
    )
    visits = int(result["Attributes"]["visits"])

    # CORS headers are added by the function URL settings, not here.
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"visits": visits}),
    }
