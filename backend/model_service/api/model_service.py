from fastapi import APIRouter
from ..service.model_service import Model_Service

router = APIRouter()

service = Model_Service()


@router.post("/model_service")
def model_service_endpoint(data: dict):
    result = service.predict(data)
    return {"Prediction_Score": result}
