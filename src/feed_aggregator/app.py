import os
from fastapi import FastAPI

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

from feed_aggregator.routes import register_routes
from feed_aggregator.middlewares import SecureServerHeadersMiddleware
from feed_aggregator.exceptions import configure_exception_handlers


class APIAppBuilder:
    
    @classmethod
    def build_app(cls) -> FastAPI:
        """
        Build and configure the FastAPI application.
        
        Returns:
            FastAPI: Configured FastAPI application instance
        """
        debug_mode = os.getenv("DEBUG", "false").lower() == "true"
        
        if debug_mode:
            print("Debug mode is enabled")
        
        app = FastAPI(
            docs_url=None,
            redoc_url=None,
            openapi_url=None,
            default_response_class=None,
            debug=debug_mode
        )
        
        register_routes(app)
        cls._configure_middleware(app)
        cls._configure_exception_handlers(app)
        
        return app
    
    @staticmethod
    def _configure_middleware(app: FastAPI) -> None:
        """Configure all middleware for the application."""
        
        # Rate limiting
        limiter = Limiter(key_func=get_remote_address)
        app.state.limiter = limiter
        app.add_middleware(SlowAPIMiddleware)

        # Security headers
        app.add_middleware(SecureServerHeadersMiddleware)
    
    @staticmethod
    def _configure_exception_handlers(app: FastAPI) -> None:
        """Configure exception handlers for the application."""
        # Use the centralized exception handler configuration
        configure_exception_handlers(app)


app = APIAppBuilder.build_app()