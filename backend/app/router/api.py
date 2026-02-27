from fastapi import FastAPI
from ..router import serviceendpoint
app = FastAPI()

app.include_router(router=serviceendpoint.router, prefix="/api/v1")

# uvicorn backend.app.router.api:app --reload --port 8002
