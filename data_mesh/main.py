import uvicorn
from api.quality_service import app

def main():
    """Run the data quality service."""
    uvicorn.run(
        "api.quality_service:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main() 