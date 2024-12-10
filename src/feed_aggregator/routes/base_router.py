from fastapi import APIRouter, Depends
from typing import Optional, List, Dict, Any
from dataclasses import dataclass


@dataclass
class RouterConfig:
    """Configuration for router creation."""
    tag: str
    prefix: Optional[str] = None
    custom_dependencies: Optional[List[Depends]] = None
    custom_responses: Optional[Dict[int, Dict[str, Any]]] = None


class APIRouterFactory:
     # Standard error responses
    _BASE_RESPONSES = {
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
        503: {"description": "Service unavailable"}
    }
    
    @classmethod
    def create_router(cls, config: RouterConfig) -> APIRouter:
        """
        Create a router with standardized security settings.
        
        Args:
            config: Router configuration
            
        Returns:
            APIRouter: Configured router instance
            
        Example:
            >>> config = RouterConfig(
            ...     tag="users",
            ...     prefix="/users"
            ... )
            >>> router = RouterFactory.create_router(config)
        """
        # Combine base responses with custom ones
        responses = {
            **cls._BASE_RESPONSES,
            **(config.custom_responses or {})
        }
        
        return APIRouter(
            prefix=config.prefix,
            tags=[config.tag],
            responses=responses
        )