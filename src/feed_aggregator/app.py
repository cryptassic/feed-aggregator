from fastapi import FastAPI

from feed_aggregator.routes import register_routes


class APIAppBuilder:
    
    @classmethod
    def build_app(cls) -> FastAPI:
        """
        Build and configure the FastAPI application.
        
        Returns:
            FastAPI: Configured FastAPI application instance
        """
        app = FastAPI(
            docs_url=None,
            redoc_url=None,
            openapi_url=None,
        )
        
        register_routes(app)
        
        return app
    
    @staticmethod
    def _configure_middleware(app: FastAPI) -> None:
        """Configure all middleware for the application."""
        pass
    
    @staticmethod
    def _configure_exception_handlers(app: FastAPI) -> None:
        """Configure exception handlers for the application."""
        pass
    
app = APIAppBuilder.build_app()