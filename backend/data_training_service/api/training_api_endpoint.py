from fastapi import APIRouter
from backend.data_training_service.service.datatraining import DataTrainingService

router = APIRouter()
service = DataTrainingService()


@router.post("/DatatrainingService")
def data_preprocessing_service_excuter():
    service.kafka_broker()
    print("service2 over and out")
