from fastapi import APIRouter
from . import conversion

router = APIRouter()
# Include the legacy endpoint directly at /api level
router.include_router(conversion.legacy_router)
# Include the new endpoints under /conversion
router.include_router(conversion.router, prefix="/conversion", tags=["conversion"])