from fastapi.responses import JSONResponse
from fastapi import status

from typing import Dict
from .base_router import APIRouterFactory, RouterConfig

from feed_aggregator.exceptions import _create_error_response

router = APIRouterFactory.create_router(
    RouterConfig(
        tag="test",
        prefix="/test"
    )
)

@router.get("")
async def get_test()-> JSONResponse:
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": "Test endpoint reached",
            "data": {
                "test": "value"
            }
        }
    )
