# Step-by-Step Zapier Integration Setup

Follow these steps to create your MovieFan Zapier integration.

## Prerequisites Checklist

- [x] Node.js installed (v24.12.0)
- [ ] Zapier account created
- [ ] MovieFan API running on http://localhost:8001
- [ ] API key from MovieFan

---

## Step 1: Install Zapier CLI

```bash
npm install -g zapier-platform-cli
```

**Verify installation:**
```bash
zapier --version
```

**Expected output:** Version number (e.g., `15.0.0`)

---

## Step 2: Login to Zapier

```bash
zapier login
```

**What happens:**
1. Opens your browser
2. Logs you into Zapier
3. Authorizes the CLI

**Expected output:** `✓ Logged in as your-email@example.com`

---

## Step 3: Navigate to Zapier App Directory

The Zapier app is already created in your MovieFan project:

```bash
cd /Users/carlosgarcia/Documents/Code/MovieFan/zapier-app
```

---

## Step 4: Install Dependencies

```bash
npm install
```

This installs `zapier-platform-core` and other dependencies.

---

## Step 5: Get Your MovieFan API Key

Before testing, you need an API key:

1. **Start your MovieFan backend** (if not running):
   ```bash
   cd /Users/carlosgarcia/Documents/Code/MovieFan
   python3 run.py
   ```

2. **Login to get a JWT token:**
   ```bash
   curl -X POST "http://localhost:8001/api/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=your_username&password=your_password"
   ```

3. **Get your API key:**
   ```bash
   curl -X GET "http://localhost:8001/api/zapier/api-key" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

4. **Save the API key** - you'll need it for testing.

---

## Step 6: Test Authentication

Create a test file `test-auth.js`:

```javascript
const zapier = require('zapier-platform-core');
const App = require('./index');

const appTester = zapier.createAppTester(App);

const testAuth = async () => {
  const bundle = {
    authData: {
      apiKey: 'YOUR_API_KEY_HERE',
      apiUrl: 'http://localhost:8001'
    }
  };
  
  try {
    const result = await appTester(App.authentication.test, bundle);
    console.log('✓ Authentication successful!', result);
  } catch (error) {
    console.error('✗ Authentication failed:', error.message);
  }
};

testAuth();
```

Or use Zapier's built-in test:

```bash
zapier test auth
```

**When prompted:**
- API Key: Your MovieFan API key
- API URL: `http://localhost:8001`

---

## Step 7: Test Triggers

### Test New Room Trigger

```bash
zapier test trigger newRoom
```

**When prompted:**
- API Key: Your MovieFan API key
- API URL: `http://localhost:8001`

### Test New Review Trigger

```bash
zapier test trigger newReview
```

---

## Step 8: Test Actions

### Test Create Room Action

```bash
zapier test create createRoom
```

**When prompted, provide:**
- API Key: Your MovieFan API key
- API URL: `http://localhost:8001`
- Room Name: "Test Room"
- Movie ID: 1 (or any existing movie ID)
- Description: "Test description"
- Private Room: false
- Max Members: 50

### Test Create Review Action

```bash
zapier test create createReview
```

**When prompted, provide:**
- API Key: Your MovieFan API key
- API URL: `http://localhost:8001`
- Movie ID: 1
- Rating: 9
- Review Text: "Great movie!"

### Test Search Movies

```bash
zapier test search searchMovies
```

**When prompted, provide:**
- API Key: Your MovieFan API key
- API URL: `http://localhost:8001`
- Search Query: "matrix"
- Limit: 10

---

## Step 9: Register Your App on Zapier

```bash
zapier register
```

**What happens:**
1. Prompts for app title: `MovieFan`
2. Prompts for app description
3. Creates your app on Zapier platform
4. Returns your app ID

**Save the app ID** - you'll need it for pushing updates.

---

## Step 10: Push Your App to Zapier

```bash
zapier push
```

**What happens:**
1. Validates your app
2. Uploads to Zapier
3. Makes it available in your Zapier account

**Expected output:**
```
✓ Pushed version 1.0.0
```

---

## Step 11: Test in Zapier Web Interface

1. Go to https://zapier.com/apps
2. Find "MovieFan" in your apps
3. Click "Create Zap"
4. Test each trigger and action

---

## Step 12: Create Your First Zap (Example)

**Example: When New Room Created → Send Slack Message**

1. **Trigger:** MovieFan - New Room
2. **Action:** Slack - Send Channel Message
3. **Map fields:**
   - Channel: #general
   - Message: "New room created: {{room_name}} for {{movie_title}}"

---

## Troubleshooting

### Authentication Fails

**Check:**
- MovieFan API is running on port 8001
- API key is correct
- API URL is correct (http://localhost:8001)

**Test manually:**
```bash
curl -X GET "http://localhost:8001/api/zapier/test" \
  -H "X-API-Key: YOUR_API_KEY"
```

### Triggers Don't Work

**Check:**
- Webhook subscription was created
- MovieFan backend is receiving webhook requests
- Check MovieFan logs for errors

### Actions Fail

**Check:**
- Required fields are provided
- Movie ID exists in database
- User has permission (API key is valid)

---

## File Structure

```
zapier-app/
├── index.js              # Main app definition
├── package.json          # Dependencies
├── authentication.js     # Auth config
├── triggers/
│   ├── newRoom.js        # New room trigger
│   └── newReview.js      # New review trigger
├── creates/
│   ├── createRoom.js     # Create room action
│   └── createReview.js   # Create review action
└── searches/
    └── searchMovies.js   # Search movies action
```

---

## Next Steps

1. ✅ Test all triggers and actions locally
2. ✅ Push to Zapier
3. ✅ Test in Zapier web interface
4. ✅ Create example Zaps
5. ⏳ Submit for public release (optional)

---

## Quick Reference

```bash
# Install CLI
npm install -g zapier-platform-cli

# Login
zapier login

# Test
zapier test auth
zapier test trigger newRoom
zapier test create createRoom

# Register & Push
zapier register
zapier push
```


