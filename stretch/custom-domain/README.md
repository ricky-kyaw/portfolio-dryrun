# Stretch goal 4: your own domain name (demo, costs money)

Swap `main.d1abc2def3.amplifyapp.com` for something like `yourname.dev`. **This costs money**: you pay to register the domain each year, and a Route 53 hosted zone has a small monthly charge. In the workshop, the facilitator demos it; do it yourself only if you want to pay for a domain.

## Option A: buy the domain in Route 53

1. [Route 53 console](https://console.aws.amazon.com/route53/home) → **Registered domains** → **Register domains**. Search for a name and check the yearly price before you buy (it varies by ending, e.g. `.com`, `.dev`).
2. Registration can take a few minutes to a few hours. Route 53 creates a hosted zone for it automatically.
3. [Amplify console](https://console.aws.amazon.com/amplify/apps) → your app → **Hosting** → **Custom domains** → **Add domain**.
4. Pick your domain from the list. Amplify sets up the DNS records and a free SSL certificate for you.
5. Wait for the status to reach **Available**, then open `https://yourname.dev`.

## Option B: domain bought somewhere else

1. In Amplify → **Custom domains** → **Add domain**, type your domain.
2. Amplify shows the DNS records to add. Copy them into your registrar's DNS settings.
3. Wait for verification (can take up to a day while DNS updates).

## Clean up

Removing the domain from Amplify doesn't cancel the registration. In Route 53, turn off **auto-renew** if you don't want to pay again next year, and delete the hosted zone if you no longer use the domain.
