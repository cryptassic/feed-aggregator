import uvicorn
from feed_aggregator.app import APIAppBuilder


def main():
    """Entry point for the application."""
    
    uvicorn.run(
        "feed_aggregator.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        workers=4,
        log_level="info"
    )


if __name__ == "__main__":
    main()