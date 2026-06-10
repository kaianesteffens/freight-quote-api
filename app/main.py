from fastapi import FastAPI

from app.config import get_settings
from app.routers import addresses, auth, quotes

settings = get_settings()

app = FastAPI(title=settings.app_name)

app.include_router(auth.router)
app.include_router(quotes.router)
app.include_router(addresses.router)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
