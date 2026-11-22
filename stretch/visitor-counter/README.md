# Stretch goal 1: visitor counter

Add "You are visitor #123" to your site using **AWS Lambda** (runs your code) and **Amazon DynamoDB** (stores the count). About 20 minutes.

```
Your site (Amplify) ──fetch──▶ Lambda function URL ──▶ Lambda ──▶ DynamoDB table
```

Use the **same AWS Region** for every step (for example Europe (London) `eu-west-2`). The Region menu is at the top right of the console.

## 1. Create the table

1. Open the [DynamoDB console](https://console.aws.amazon.com/dynamodbv2/home) → **Tables** → **Create table**.
2. Table name: `visitor-count`. Partition key: `id`, type **String**.
3. Table settings: choose **Customize settings** → Capacity mode **Provisioned** → Read capacity **1**, Write capacity **1**, auto scaling **Off** for both. This stays inside DynamoDB's always-free allowance.
4. **Create table**. When it's Active, open it and copy its **ARN** from *General information*.

## 2. Create the function

1. Open the [Lambda console](https://console.aws.amazon.com/lambda/home) → **Create function** → **Author from scratch**.
2. Name: `visitor-counter`. Runtime: **Python 3.13**. Leave the rest as default → **Create function**.
3. In the **Code** tab, replace everything in `lambda_function.py` with [this folder's `lambda_function.py`](lambda_function.py) → **Deploy**.
4. **Configuration** → **Environment variables** → **Edit** → add `TABLE_NAME` = `visitor-count` → **Save**.

## 3. Let the function write to the table

1. **Configuration** → **Permissions** → click the **Role name** (opens IAM).
2. **Add permissions** → **Create inline policy** → **JSON**, paste this, and replace the ARN with the one you copied:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "dynamodb:UpdateItem",
      "Resource": "arn:aws:dynamodb:REGION:ACCOUNT_ID:table/visitor-count"
    }
  ]
}
```

3. **Next** → name it `visitor-counter-dynamodb` → **Create policy**.

## 4. Give the function a public URL

1. Back in Lambda: **Configuration** → **Function URL** → **Create function URL**.
2. Auth type: **NONE**.
3. Expand **Additional settings** → tick **Configure cross-origin resource sharing (CORS)**:
   - Allow origin: your Amplify URL, e.g. `https://main.d1abc2def3.amplifyapp.com` (no slash at the end)
   - Allow methods: `GET`
4. **Save**, then copy the **Function URL**.
5. Paste the URL into your browser. You should see `{"visits": 1}`. Refresh and it goes up.

## 5. Show it on your site

1. Open `site/config.js` and paste the URL into `VISITOR_COUNTER_URL`.
2. Commit the change. Amplify redeploys, and your site shows the count under your links.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| Browser shows `Forbidden` / 403 | Configuration → Permissions → Resource-based policy must allow both `lambda:InvokeFunctionUrl` and `lambda:InvokeFunction`. Add the missing one with **Add permissions** → **Function URL**. |
| Browser shows `Internal Server Error` | Open the **Monitor** tab → **View CloudWatch logs**. `AccessDeniedException` means step 3 isn't done or the ARN is wrong. `ResourceNotFoundException` means the table name or Region doesn't match. |
| URL works but the site shows nothing | Press F12 → Console. A CORS error means the Allow origin doesn't exactly match your Amplify URL. |
