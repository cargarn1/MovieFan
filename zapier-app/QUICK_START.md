# Quick Start - Zapier Integration

## Using Zapier CLI (Local Installation)

Since Zapier CLI is installed locally (not globally), use `npx zapier` instead of `zapier`.

## Step 1: Login to Zapier

```bash
cd /Users/carlosgarcia/Documents/Code/MovieFan/zapier-app
npx zapier login
```

This opens your browser to authenticate.

## Step 2: Test Authentication

First, make sure your MovieFan API is running:
```bash
# In another terminal
cd /Users/carlosgarcia/Documents/Code/MovieFan
python3 run.py
```

Then get your API key:
1. Login to MovieFan: http://localhost:8001
2. Get API key: http://localhost:8001/api/zapier/api-key

Test authentication:
```bash
npx zapier test auth
```

**When prompted:**
- API Key: `your-api-key-here`
- API URL: `http://localhost:8001`

## Step 3: Test Triggers

```bash
npx zapier test trigger newRoom
npx zapier test trigger newReview
```

## Step 4: Test Actions

```bash
npx zapier test create createRoom
npx zapier test create createReview
npx zapier test search searchMovies
```

## Step 5: Register Your App

```bash
npx zapier register
```

Follow the prompts to create your app on Zapier.

## Step 6: Push to Zapier

```bash
npx zapier push
```

## Alternative: Use npm scripts

You can also add scripts to `package.json`:

```json
{
  "scripts": {
    "zapier:login": "zapier login",
    "zapier:test": "zapier test",
    "zapier:register": "zapier register",
    "zapier:push": "zapier push"
  }
}
```

Then run:
```bash
npm run zapier:login
npm run zapier:test
```



