# Stretch goal 3: host it the manual way (S3 + CloudFront)

Amplify hides the plumbing. Here you build it yourself: **Amazon S3** stores the files, and **Amazon CloudFront** serves them worldwide over HTTPS. About 20 minutes (CloudFront takes a few minutes to deploy).

```
Visitor ──HTTPS──▶ CloudFront (CDN) ──private access──▶ S3 bucket (your site/ files)
```

## 1. Create a private bucket

1. Open the [S3 console](https://console.aws.amazon.com/s3/home) → **Create bucket**.
2. Bucket name: must be unique across all of AWS, e.g. `yourname-portfolio-2026`.
3. Leave **Block all public access** turned **on**. CloudFront will read the files privately.
4. **Create bucket**.

## 2. Upload the site

1. Open the bucket → **Upload** → **Add files**.
2. Select everything **inside** your `site/` folder (`index.html`, `styles.css`, `script.js`, `config.js`, `favicon.svg`), not the folder itself.
3. **Upload**.

## 3. Put CloudFront in front

1. Open the [CloudFront console](https://console.aws.amazon.com/cloudfront/v4/home) → **Create distribution**.
2. If you're asked to pick a pricing plan and a flat-rate **Free** plan is offered, choose it.
3. Origin: choose **Amazon S3** and select your bucket. Allow CloudFront to use **origin access control** (the console's recommended private access) and let it **update the bucket policy** for you.
4. Set **Default root object** to `index.html` (if you don't see it during creation, set it afterwards under **General** → **Settings** → **Edit**).
5. Create the distribution and wait until **Last modified** shows a date instead of "Deploying".
6. Open the **Distribution domain name** (`https://d1234abcd.cloudfront.net`). That's your site.

## 4. Updating

There's no automatic deploy here: upload changed files to S3 again. CloudFront may keep showing the old version for a while because it caches files. To force an update, go to **Invalidations** → **Create invalidation** → `/*`.

## What you learned

Amplify Hosting does all of this for you, plus the Git-based redeploys. Now you know what's underneath.

## Clean up

1. CloudFront: select the distribution → **Disable**, wait for it to finish, then **Delete**.
2. S3: open the bucket → **Empty** → then **Delete** the bucket.
