# Stretch goal 2: contact form

Let visitors send you a message. The form posts to **AWS Lambda**, which checks the input and saves it to **Amazon DynamoDB**. About 20 minutes; easier if you've done the visitor counter first.

```
Contact form (Amplify) ──POST──▶ Lambda function URL ──▶ Lambda (validates) ──▶ DynamoDB table
```

Use the same AWS Region as your other stretch goals.

## 1. Create the table

1. [DynamoDB console](https://console.aws.amazon.com/dynamodbv2/home) → **Create table**.
2. Table name: `contact-messages`. Partition key: `id`, type **String**.
3. **Customize settings** → **Provisioned**, Read **1**, Write **1**, auto scaling **Off** → **Create table**. Copy its **ARN**.

## 2. Create the function

1. [Lambda console](https://console.aws.amazon.com/lambda/home) → **Create function** → **Author from scratch**.
2. Name: `contact-form`. Runtime: **Python 3.13** → **Create function**.
3. Replace `lambda_function.py` with [this folder's `lambda_function.py`](lambda_function.py) → **Deploy**.
4. **Configuration** → **Environment variables** → add `TABLE_NAME` = `contact-messages`.

## 3. Let it write to the table

**Configuration** → **Permissions** → click the role → **Add permissions** → **Create inline policy** → **JSON**:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "dynamodb:PutItem",
      "Resource": "arn:aws:dynamodb:REGION:ACCOUNT_ID:table/contact-messages"
    }
  ]
}
```

Replace the ARN with yours, name it `contact-form-dynamodb`, and create it.

## 4. Function URL

1. **Configuration** → **Function URL** → **Create function URL** → Auth type **NONE**.
2. **Configure CORS**:
   - Allow origin: your Amplify URL (no slash at the end)
   - Allow methods: `POST`
   - Allow headers: `content-type`
3. **Save** and copy the URL.

## 5. Turn on the form

1. Paste the URL into `CONTACT_FORM_URL` in `site/config.js` and commit.
2. After Amplify redeploys, a **Get in touch** section appears on your site. Send yourself a test message.
3. Read messages in DynamoDB → `contact-messages` → **Explore table items**.

## What the code protects against

- Rejects anything that isn't a POST with JSON.
- Requires name, email and message, with length limits (100 / 200 / 2000 characters).
- A hidden "website" field catches simple spam bots: if it's filled in, nothing is saved.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| "Sorry, something went wrong" | F12 → Console and Network. A CORS error: check Allow origin, methods `POST` and header `content-type`. |
| 403 Forbidden | Resource-based policy needs both `lambda:InvokeFunctionUrl` and `lambda:InvokeFunction`. |
| 500 error | Monitor → CloudWatch logs. Usually the inline policy (step 3) or the table name. |

## Want an email for each message?

Amazon SES can email you, but new SES accounts start in a "sandbox" and need your email address verified first. Treat it as a follow-up project.
