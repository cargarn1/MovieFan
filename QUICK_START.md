# Quick Start Guide

## Running the Application

### Step 1: Start the Backend API Server

Open Terminal 1:
```bash
cd /Users/carlosgarcia/Documents/Code/MovieFan
python3 run.py
```

Backend will run on: **http://localhost:5001**

### Step 2: Start the Frontend

Open Terminal 2:
```bash
cd /Users/carlosgarcia/Documents/Code/MovieFan/frontend
npm run dev
```

Frontend will run on: **http://localhost:8001**

### Step 3: Open in Browser

Visit: **http://localhost:8001**

## First Time Setup

If you haven't initialized the database yet:
```bash
python3 -m app.init_db
```

## What You'll See

1. **Home Page** - Welcome screen with featured movies
2. **Register/Login** - Create an account or sign in
3. **Movies** - Browse and search movies
4. **Rooms** - Join discussion rooms
5. **Recommendations** - Get personalized movie suggestions (requires login)

## Troubleshooting

### Backend won't start
- Check if port 5001 is available
- Make sure `.env` file exists
- Verify database is initialized: `python3 -m app.init_db`

### Frontend won't start
- Make sure you're in the `frontend` directory
- Try: `npm install` again
- Check if port 8001 is available

### Can't connect to API
- Make sure backend is running on port 5001
- Check browser console for errors
- Verify CORS is enabled in backend

## Stopping the Servers

Press `CTRL+C` in each terminal to stop the servers.

