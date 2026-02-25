from fastapi import APIRouter
from backend.data_preprocessing_service.service.datatprocess import DataPreprocessingService

router = APIRouter()
service = DataPreprocessingService()


@router.post("/DataPreprocessingService")
def data_preprocessing_service_excuter():
    service.process_the_data()
    print("service 1 over and out")
