# How to Start the Servers

## Quick Start

You need **TWO separate terminal windows** to run both servers.

### Terminal 1 - Backend API Server

```bash
cd /Users/carlosgarcia/Documents/Code/MovieFan
python3 run.py
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:5001 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Keep this terminal open!** The server needs to keep running.

### Terminal 2 - Frontend Server

```bash
cd /Users/carlosgarcia/Documents/Code/MovieFan/frontend
npm run dev
```

**Expected output:**
```
  VITE v5.0.8  ready in XXX ms

  ➜  Local:   http://localhost:5000/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**Keep this terminal open too!**

## Verify Servers Are Running

Open your browser and visit:
- **Frontend:** http://localhost:5000
- **Backend API:** http://localhost:5001
- **API Docs:** http://localhost:5001/docs

## Troubleshooting

### Backend won't start

1. **Check if port 5001 is in use:**
   ```bash
   lsof -i :5001
   # If something is using it, kill it:
   kill -9 <PID>
   ```

2. **Install missing dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Check .env file exists:**
   ```bash
   ls -la .env
   ```

### Frontend won't start

1. **Check if port 5000 is in use:**
   ```bash
   lsof -i :5000
   # If something is using it, kill it:
   kill -9 <PID>
   ```

2. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

3. **Check Node.js is installed:**
   ```bash
   node --version
   npm --version
   ```

## Stopping the Servers

Press `CTRL+C` in each terminal window to stop the servers.

