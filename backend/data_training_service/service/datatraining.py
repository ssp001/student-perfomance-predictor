import threading  # 1. Import threading
import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from confluent_kafka import Consumer
import numpy as np
import json
import logging
import joblib
import time
logger = logging.getLogger(__name__)


class DataTrainingService:
    def __init__(self):
        # ... your existing init (engine, consumer, etc.) ...
        kafka_consumer_config = {'bootstrap.servers': 'localhost:9092',
                                 'group.id': 'service-2',
                                 'enable.auto.commit': False,
                                 'auto.offset.reset': 'earliest',
                                 'max.poll.interval.ms': 600000,
                                 'session.timeout.ms': 45000
                                 }
        self.consumer = Consumer(kafka_consumer_config)
        self.consumer.subscribe(["mlpipeline"])
        self.engine = create_engine(
            "postgresql+psycopg2://ssp001:shovansaha1234@localhost:5433/dataset_db"
        )
        data_set = pd.read_sql(
            "SELECT * FROM student_performance_dataset", self.engine)
        self.x = data_set.iloc[:, :-1]
        self.y = data_set.iloc[::, -1]
        self.rfr = RandomForestRegressor(n_estimators=500,
                                         max_depth=15,
                                         min_samples_split=5,
                                         random_state=42)
        self.path = "backend/model_service/model"

    def train_the_model(self):
        try:
            x_train, x_test, y_train, y_test = train_test_split(
                self.x, self.y, test_size=0.2, random_state=42)
            self.rfr.fit(x_train, y_train)
            y_pred = self.rfr.predict(x_test)
            mae = mean_absolute_error(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test, y_pred)
            logger.info(mae, mse, rmse, r2)
            joblib.dump(
                self.rfr, "C:/Users/shova/Desktop/project/student performance detector/backend/model_service/model/model_predictor.pkl")
            logger.info(f"model saved to the path succesfully:{self.path}")
        except Exception as e:
            logger.error(
                f"there is a error in {self.train_the_model()} function:{e}")
            raise RuntimeError(
                f"there is a error in {self.train_the_model()} function:{e}")

    def kafka_broker(self):
        try:
            while True:
                msg = self.consumer.poll(1.0)
                data = msg.value()
                if data is None:
                    offset = json.load(data)
                    continue
                if msg.error():
                    print(msg.error())
                    continue
                if msg.value() == "Data preProcessing task complete":
                    self.train_the_model()
                    logger.info(
                        f"{self.train_the_model()}function has started")
        except Exception as e:
            logger.error(f"there is a error in{self.kafka_broker()}:{e}")
            raise RuntimeError(f"there is a error in{self.kafka_broker()}:{e}")
        finally:
            self.consumer.close()
