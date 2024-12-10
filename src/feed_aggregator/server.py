import os
import uvicorn

def main():
    """Entry point for the application."""
    
    uvicorn.run(
        "feed_aggregator.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        workers=4,
        log_level="debug" if os.getenv("DEBUG", "info").lower() == "debug" else "info",
        server_header=False,
    )


if __name__ == "__main__":
    main()