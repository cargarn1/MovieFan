"""Quick start script for the MovieFan API."""
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    # Get port from environment variable or default to 5001
    port = int(os.getenv("PORT", 5001))
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )

