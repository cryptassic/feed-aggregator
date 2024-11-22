from fastapi import FastAPI, APIRouter
from typing import Dict

from .base_router import APIRouterFactory, RouterConfig

# Import all route modules
from .default import router as default_router



class RouterRegistry:
    """Registry for managing all API routes."""
    
    AVAILABLE_ROUTES: Dict[str, APIRouter] = {
        "health": default_router,
        # Add new routers here with their identifiers
    }
    
    @classmethod
    def create_main_router(cls) -> APIRouter:
        """
        Create main router with all registered subrouters.
        
        Returns:
            APIRouter: Configured main router with all routes
        """
        # main_router = APIRouter(
        #     prefix="/v1",
        #     responses={
        #         404: {"description": "Not found"},
        #         500: {"description": "Internal server error"},
        #         503: {"description": "Service unavailable"}
        #     }
        # )
        
        main_router = APIRouterFactory.create_router(RouterConfig(
            tag="root",
            prefix="/v1"
        ))
        
        # Include all available routers
        for router in cls.AVAILABLE_ROUTES.values():
            main_router.include_router(router)
            
        return main_router


def register_routes(app: FastAPI) -> None:
    """
    Register all route handlers to the FastAPI application.
    
    Args:
        app (FastAPI): The FastAPI application instance
    """
    main_router = RouterRegistry.create_main_router()
    app.include_router(main_router)


