# Troubleshooting Guide

## Servers Not Starting

### Backend API (Port 8001)

**Start the backend:**
```bash
cd /Users/carlosgarcia/Documents/Code/MovieFan
python3 run.py
```

**Check if it's running:**
```bash
curl http://localhost:5001/health
```

**Common issues:**
1. **Port already in use:**
   ```bash
   lsof -i :5001
   # Kill the process if needed
   kill -9 <PID>
   ```

2. **Missing dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Database not initialized:**
   ```bash
   python3 -m app.init_db
   ```

4. **Missing .env file:**
   ```bash
   # Create .env file with required variables
   cat .env
   ```

### Frontend (Port 5001)

**Start the frontend:**
```bash
cd /Users/carlosgarcia/Documents/Code/MovieFan/frontend
npm run dev
```

**Check if it's running:**
```bash
curl http://localhost:5001
```

**Common issues:**
1. **Port already in use:**
   ```bash
   lsof -i :5001
   # Kill the process if needed
   kill -9 <PID>
   ```

2. **Missing dependencies:**
   ```bash
   cd frontend
   npm install
   ```

3. **Node.js not in PATH:**
   ```bash
   which node
   which npm
   # If not found, add to PATH or reinstall Node.js
   ```

## Both Servers Must Run Simultaneously

You need **TWO terminal windows**:

**Terminal 1 - Backend:**
```bash
cd /Users/carlosgarcia/Documents/Code/MovieFan
python3 run.py
```

**Terminal 2 - Frontend:**
```bash
cd /Users/carlosgarcia/Documents/Code/MovieFan/frontend
npm run dev
```

## Verify Servers Are Running

```bash
# Check backend
curl http://localhost:5001/health
# Should return: {"status":"healthy"}

# Check frontend
curl http://localhost:5001
# Should return HTML content

# Check ports are listening
lsof -i :5001
lsof -i :5001
```

## Access the Application

- **Frontend:** http://localhost:5001
- **Backend API:** http://localhost:8001
- **API Docs:** http://localhost:8001/docs

## Still Having Issues?

1. Check error messages in the terminal where you started the servers
2. Verify all dependencies are installed
3. Check firewall settings
4. Try restarting your computer
5. Check if antivirus is blocking the ports

