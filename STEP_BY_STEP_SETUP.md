# Step-by-Step Setup Guide for MovieFan

Follow these steps in order to get your MovieFan API running.

## Prerequisites Check

✅ **Python 3.8+** - You have Python 3.9.6 (Good!)
✅ **pip** - Package installer available
✅ **Git** - Repository is set up

---

## Step 1: Install Python Dependencies

Install all required packages:

```bash
pip3 install -r requirements.txt
```

**What this does:** Installs FastAPI, SQLAlchemy, JWT libraries, and other dependencies.

**Expected output:** Packages downloading and installing.

---

## Step 2: Create Environment Variables File

Create a `.env` file in the project root:

```bash
touch .env
```

Then add this content to `.env`:

```env
# Database
DATABASE_URL=sqlite:///./moviefan.db

# JWT Secret Key (change this in production!)
SECRET_KEY=your-secret-key-change-this-to-something-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# TMDB API Key (get one free at https://www.themoviedb.org/settings/api)
TMDB_API_KEY=your_tmdb_api_key_here

# Server Port (API server defaults to 5001, Frontend uses 8001)
PORT=5001
```

**What this does:** Configures database, security keys, and API settings.

**Note:** You'll need to get a TMDB API key in the next step.

---

## Step 3: Get TMDB API Key (Optional but Recommended)

1. Go to https://www.themoviedb.org/
2. Click **"Sign Up"** (top right)
3. Create a free account
4. Once logged in, go to **Settings** → **API**
5. Click **"Request an API Key"**
6. Select **"Developer"** option
7. Fill out the form (use your personal info)
8. Accept terms and submit
9. Copy your **API Key** (looks like: `abc123def456...`)
10. Update your `.env` file: Replace `your_tmdb_api_key_here` with your actual key

**What this does:** Enables movie search and import from The Movie Database.

**Note:** You can skip this step if you only want to use manually added movies.

---

## Step 4: Generate a Secret Key

Generate a random secret key for JWT tokens:

**Option A - Using Python:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Option B - Using OpenSSL:**
```bash
openssl rand -hex 32
```

Copy the output and update `SECRET_KEY` in your `.env` file.

**What this does:** Secures your JWT authentication tokens.

---

## Step 5: Initialize the Database

Create the database and add sample movies:

```bash
python3 -m app.init_db
```

**What this does:**
- Creates SQLite database file (`moviefan.db`)
- Creates all database tables (users, movies, rooms, reviews, etc.)
- Adds 10 sample movies to get you started

**Expected output:** 
```
Initializing database...
Adding sample movies...
Successfully added 10 movies to the database.
Database initialization complete!
```

---

## Step 6: Start the Server

Run the development server:

```bash
python3 run.py
```

**What this does:** Starts the FastAPI server on port 5001 (API server).

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:5001 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Keep this terminal open!** The server needs to keep running.

---

## Step 7: Verify the Server is Running

Open your browser and visit:

- **API Root:** http://localhost:5001
- **Interactive API Docs:** http://localhost:5001/docs
- **Alternative Docs:** http://localhost:5001/redoc
- **Frontend:** http://localhost:8001 (after starting frontend)

You should see:
- Root endpoint shows welcome message
- `/docs` shows Swagger UI with all API endpoints
- `/redoc` shows ReDoc documentation

---

## Step 8: Test the API

### 8.1 Register a Test User

Open a **new terminal** (keep server running) and run:

```bash
curl -X POST "http://localhost:5001/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
  }'
```

**Expected response:**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "full_name": "Test User",
  "bio": null,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### 8.2 Login

```bash
curl -X POST "http://localhost:5001/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"
```

**Expected response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

**Save the `access_token`** - you'll need it for authenticated requests!

### 8.3 Get Your API Key (for Zapier)

```bash
curl -X GET "http://localhost:5001/api/zapier/api-key" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

Replace `YOUR_ACCESS_TOKEN_HERE` with the token from step 8.2.

**Expected response:**
```json
{
  "api_key": "your-api-key-here",
  "message": "Use this API key in Zapier: X-API-Key header"
}
```

### 8.4 List Movies

```bash
curl "http://localhost:5001/api/movies"
```

You should see the 10 sample movies that were added.

---

## Step 9: Explore the API Documentation

1. Open http://localhost:5001/docs in your browser
2. Click on any endpoint to expand it
3. Click **"Try it out"** to test endpoints directly in the browser
4. For authenticated endpoints, click **"Authorize"** and paste your JWT token

---

## Troubleshooting

### Port Already in Use

If port 5001 is taken, change it in `.env`:
```env
PORT=5002
```

### Database Errors

If you get database errors, delete and recreate:
```bash
rm moviefan.db
python3 -m app.init_db
```

### Import Errors

If `pip3 install` fails:
- Try: `pip install -r requirements.txt`
- Or: `python3 -m pip install -r requirements.txt`

### TMDB API Errors

If TMDB endpoints don't work:
- Check your `.env` file has `TMDB_API_KEY` set
- Verify the API key is correct
- Make sure you're connected to the internet

---

## Next Steps

✅ **Server is running!** You can now:
- Build a frontend application
- Create Zapier integrations
- Add more movies via TMDB
- Create rooms and reviews
- Explore all API endpoints

📚 **Documentation:**
- `README.md` - Overview and features
- `API_EXAMPLES.md` - More API usage examples
- `ZAPIER_INTEGRATION.md` - Zapier setup guide

---

## Quick Reference

**Start server:**
```bash
python3 run.py
```

**Stop server:**
Press `CTRL+C` in the terminal running the server

**Reset database:**
```bash
rm moviefan.db && python3 -m app.init_db
```

**View logs:**
Server logs appear in the terminal where you ran `python3 run.py`

