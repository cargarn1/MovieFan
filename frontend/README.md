# MovieFan Frontend

React + Vite frontend for MovieFan API.

## Setup

1. **Install dependencies:**
```bash
npm install
```

2. **Start development server:**
```bash
npm run dev
```

The frontend will run on http://localhost:8001

## Features

- 🎬 Movie browsing and search
- 👤 User authentication (login/register)
- 🏠 Room creation and management
- ⭐ Movie reviews and ratings
- 🎯 Personalized recommendations
- 📱 Responsive design

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool
- **React Router** - Routing
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **Lucide React** - Icons

## API Configuration

The frontend connects to the backend API at `http://localhost:5001` (configured via proxy in `vite.config.js`).

To change the API URL, update `src/config.js`.

