# AWS Student Builder Group: Portfolio Starter

Build your own portfolio website and put it live on the internet with **AWS Amplify Hosting**. No framework and no build tools: plain HTML, CSS and JavaScript.

By the end of the workshop you'll have:

- A personal portfolio at a public `https://…amplifyapp.com` URL
- Automatic deploys: every commit to GitHub updates your live site
- Optional: a visitor counter and contact form running on AWS Lambda and DynamoDB

## What's in this repo

```
site/                  ← your website (this is what gets published)
  index.html           ← EDIT: your name, bio, skills, projects
  styles.css           ← EDIT: colours at the top of the file
  config.js            ← stretch goals only: paste your Lambda URLs here
  script.js            ← no need to edit
  favicon.svg
amplify.yml            ← tells Amplify to publish the site/ folder
stretch/
  visitor-counter/     ← Stretch 1: Lambda + DynamoDB visitor count
  contact-form/        ← Stretch 2: Lambda + DynamoDB contact form
  s3-cloudfront/       ← Stretch 3: host it the manual way
  custom-domain/       ← Stretch 4: your own domain (costs money)
```

## Before the workshop

You need:

1. A laptop and charger
2. A [GitHub account](https://github.com/signup)
3. An [AWS account](https://aws.amazon.com/free/) you can sign in to. New accounts choose the **Free plan**.

## The main build

### Part A: make it yours (20 min)

1. On this repo's GitHub page, click **Use this template** → **Create a new repository**. Name it `portfolio`, keep it **Public**, and create it.
2. In your new repo, open `site/index.html` and click the pencil icon to edit. Search for `EDIT ME` and replace the placeholder text with your own details.
3. Click **Commit changes**.
4. Optional: open `site/styles.css` and change the colours at the top.

Tip: press `.` on your repo page to open a full editor in the browser.

### Part B: go live (20 min)

1. Sign in to the [AWS Amplify console](https://console.aws.amazon.com/amplify/apps).
2. Choose **Create new app** (or **Deploy an app**) → **GitHub** → **Next**.
3. Sign in to GitHub when asked and give Amplify access to your `portfolio` repo.
4. Pick the `portfolio` repo and the `main` branch → **Next**.
5. Amplify finds `amplify.yml` and fills in the build settings. Leave them as they are → **Next** → **Save and deploy**.
6. Wait about a minute until every step is green, then open the URL ending in `amplifyapp.com`. Your site is live.

### Part C: ship an update (10 min)

1. Edit any line in `site/index.html` on GitHub and commit.
2. Go back to Amplify. A new deploy starts by itself.
3. Refresh your site after about a minute. You just used CI/CD: continuous integration and continuous delivery.

## Stretch goals

| # | Goal | Services | Time | Cost |
| --- | --- | --- | --- | --- |
| 1 | [Visitor counter](stretch/visitor-counter/README.md) | Lambda, DynamoDB | ~20 min | Free within always-free limits |
| 2 | [Contact form](stretch/contact-form/README.md) | Lambda, DynamoDB | ~20 min | Free within always-free limits |
| 3 | [Manual hosting with S3 + CloudFront](stretch/s3-cloudfront/README.md) | S3, CloudFront | ~20 min | Pennies or free |
| 4 | [Custom domain](stretch/custom-domain/README.md) | Route 53, Amplify | Demo | Costs money |

## Avoid surprise bills

- Set up a **zero spend budget**: [Billing and Cost Management](https://console.aws.amazon.com/cost-management/home) → **Budgets** → **Create budget** → **Use a template** → **Zero spend budget**. AWS emails you if you spend anything.
- When you're finished, delete what you don't want to keep:
  - Amplify: your app → **App settings** → **General settings** → **Delete app**
  - Lambda: delete `visitor-counter` and `contact-form`
  - DynamoDB: delete `visitor-count` and `contact-messages`
  - S3 and CloudFront: see the cleanup steps in `stretch/s3-cloudfront/README.md`

## Troubleshooting

| Problem | Fix |
| --- | --- |
| Amplify shows a blank page or 404 | Check `amplify.yml` is in the repo root and `baseDirectory` is `site`. |
| Amplify can't see my repo | GitHub → Settings → Applications → AWS Amplify → **Configure** → give it access to the repo. |
| My change isn't showing | Wait for the Amplify deploy to finish, then hard-refresh (`Ctrl+Shift+R` / `Cmd+Shift+R`). |
| Region confusion | Lambda and DynamoDB must be in the same Region. Check the menu at the top right of the console. |

---

Made for an AWS Student Builder Group workshop. Feel free to reuse it for your own group.
