from .base_router import APIRouterFactory, RouterConfig
from typing import Dict

router = APIRouterFactory.create_router(
    RouterConfig(
        tag="test",
        prefix="/test"
    )
)

@router.get("/")
async def hello_world()-> Dict[str, str]:
    return {"message": "Hello, World!"}