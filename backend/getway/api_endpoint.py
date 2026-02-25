from ..data_preprocessing_service.api import process_api_endpoint
from ..data_training_service.api import training_api_endpoint
from fastapi import FastAPI


app = FastAPI(name="api_getway")

app.include_router(training_api_endpoint.router,
                   prefix="/training_api_server", tags=["training_api_server"])
app.include_router(process_api_endpoint.router,
                   prefix="/process_api_server", tags=["process_api_server"])
