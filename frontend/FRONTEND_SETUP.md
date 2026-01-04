# Frontend Setup Instructions

## Prerequisites

1. **Node.js** (v16 or higher) - Download from https://nodejs.org/
2. **npm** (comes with Node.js)

## Installation Steps

### 1. Install Node.js (if not already installed)

Check if Node.js is installed:
```bash
node --version
npm --version
```

If not installed, download and install from https://nodejs.org/

### 2. Navigate to Frontend Directory

```bash
cd frontend
```

### 3. Install Dependencies

```bash
npm install
```

This will install all required packages including:
- React
- React Router
- Axios
- Tailwind CSS
- Lucide React icons

### 4. Start Development Server

```bash
npm run dev
```

The frontend will start on **http://localhost:8001**

## Development Setup

### Frontend (Port 8001)
- Runs on: http://localhost:8001
- Hot reload enabled
- Proxy configured to backend API

### Backend API (Port 5001)
- Make sure backend is running: `python3 run.py` (from project root)
- API available at: http://localhost:5001

## Building for Production

```bash
npm run build
```

This creates an optimized production build in the `dist/` directory.

## Project Structure

```
frontend/
├── src/
│   ├── components/     # Reusable components
│   │   └── layout/     # Layout components (Navbar, etc.)
│   ├── pages/          # Page components
│   ├── services/       # API service layer
│   ├── config.js       # Configuration
│   ├── App.jsx         # Main app component
│   ├── main.jsx        # Entry point
│   └── index.css       # Global styles
├── package.json        # Dependencies
├── vite.config.js      # Vite configuration
└── tailwind.config.js  # Tailwind CSS configuration
```

## Features

- ✅ User authentication (login/register)
- ✅ Movie browsing and search
- ✅ Movie detail pages with reviews
- ✅ Room creation and management
- ✅ Personalized recommendations
- ✅ User profile
- ✅ Responsive design
- ✅ Dark theme UI

## Troubleshooting

### Port 8001 Already in Use

Change the port in `vite.config.js`:
```javascript
server: {
  port: 8002,  // Change to your preferred port
}
```

### API Connection Issues

1. Make sure backend is running on port 5001
2. Check `src/config.js` for correct API URL
3. Verify CORS is enabled in backend (`app/main.py`)

### Build Errors

Clear cache and reinstall:
```bash
rm -rf node_modules package-lock.json
npm install
```

## Next Steps

1. Start backend: `python3 run.py` (from project root)
2. Start frontend: `npm run dev` (from frontend directory)
3. Open http://localhost:8001 in your browser
4. Register a new account or login
5. Explore the app!

