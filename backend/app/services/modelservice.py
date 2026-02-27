import pandas as pd
import logging
import joblib

logger = logging.getLogger(__name__)


class ModelService:
    def __init__(self):
        self.model = joblib.load(
            filename="backend/app/db/student_performance_pipeline.pkl")
        logger.info("model fetched sucesses fuly")

    def predict(self, input_data: dict):
        try:
            data_frame = pd.DataFrame([input_data])
            prediction = self.model.predict(data_frame)
            logger.info("model predict complete 😶‍🌫️")
            return float(prediction[0])

        except Exception as error:
            logger.exception(error)
            raise RuntimeError(f"an error occured in {logger}:")
