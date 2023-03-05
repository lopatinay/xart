from fastapi import APIRouter


system_router = APIRouter()


@system_router.get("/health", tags=["System"])
async def healthcheck():
    return "healthy"
