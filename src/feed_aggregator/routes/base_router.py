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
    # _SECURITY_HEADERS = {
    #     "X-Content-Type-Options": "nosniff",
    #     "X-Frame-Options": "DENY",
    #     "X-XSS-Protection": "1; mode=block",
    #     "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    # }
    
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
        
        # return APIRouter(
        #     prefix=config.prefix,
        #     tags=[config.tag],
        #     responses=responses,
        #     default_response_class=cls._create_secure_response(),
        # )
    
    @classmethod
    def _create_secure_response(cls):
        from fastapi.responses import JSONResponse
        
        class SecureJSONResponse(JSONResponse):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.headers.update(cls._SECURITY_HEADERS)
                
        return SecureJSONResponse
