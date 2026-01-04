# Frontend Setup Guide (Future)

## Current Architecture

**MovieFan currently has:**
- ✅ Backend API Server (FastAPI) - Port **8001**
- ❌ No frontend yet

## Recommended Port Setup (When Adding Frontend)

When you add a frontend application (React, Vue, Next.js, etc.), use separate ports:

### Development Setup

```
Frontend:  http://localhost:8001
Backend:   http://localhost:5001  (API server)
```

### Why Separate Ports?

1. **Different servers**: Frontend and backend run as separate processes
2. **CORS**: Backend needs to allow frontend origin
3. **Development**: Hot reload works independently
4. **Production**: Can deploy separately

## Example Frontend Frameworks

### React + Vite
```bash
npm create vite@latest frontend -- --template react
cd frontend
npm install
npm run dev  # Configured to run on port 8001
```

### Next.js
```bash
npx create-next-app@latest frontend
cd frontend
npm run dev  # Configure to run on port 8001
```

### Vue
```bash
npm create vue@latest frontend
cd frontend
npm install
npm run dev  # Configure to run on port 8001
```

## CORS Configuration

The backend already has CORS enabled for all origins in development. For production, update `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Frontend API Configuration

In your frontend, configure the API base URL:

```javascript
// config.js
export const API_BASE_URL = 'http://localhost:5001';

// Or use environment variable
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001';
```

## Current Backend Port

The API server runs on **port 5001** by default (configurable via `.env` file).

To change the API port, update `.env`:
```env
PORT=5001  # Change to your preferred port
```

