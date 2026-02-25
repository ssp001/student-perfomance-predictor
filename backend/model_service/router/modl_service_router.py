from fastapi import FastAPI
from ..api import model_service

app = FastAPI(name="router_model_endpoint")


app.include_router(model_service.router,
                   prefix="/model_service_api_server", tags=["training_api_server"])
