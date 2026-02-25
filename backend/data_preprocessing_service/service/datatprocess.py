"""DatapreprocessingService this service will clean and give the encoded data set"""

import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from confluent_kafka import Producer
from sqlalchemy import create_engine
import logging
import json

logger = logging.getLogger(__name__)


class DataPreprocessingService:
    def __init__(self):
        self.data_set = pd.read_csv(
            r"C:\Users\shova\Desktop\project\student performance detector\data\StudentPerformanceFactors.csv")
        self.ohe = OneHotEncoder(drop="first")
        kafka_config = {"bootstrap.servers": "localhost:9092"}
        self.kafka_prodcer = Producer(kafka_config)
        task = {
            "user": "servise-1",
            "message": "Data preProcessing task complete"
        }
        self.value = json.dumps(task).encode("utf-8")
        self.engine = create_engine(
            "postgresql+psycopg2://ssp001:shovansaha1234@localhost:5433/dataset_db"
        )

    def process_the_data(self) -> pd.DataFrame:
        # Dropint some null values from the data set.
        try:
            self.data_set.dropna(inplace=True)
            # performing ordinal encoding in some colums.
            ord_data = [['Low', 'Medium', 'High']]
            self.oe = OrdinalEncoder(categories=ord_data)
            self.data_set[['Parental_Involvement']] = self.oe.fit_transform(
                self.data_set[['Parental_Involvement']])
            ord_data2 = [['Low', 'Medium', 'High']]
            self.oe = OrdinalEncoder(categories=ord_data2)
            self.data_set[["Access_to_Resources"]] = self.oe.fit_transform(
                self.data_set[["Access_to_Resources"]])
            ord_data3 = [['Low', 'Medium', 'High']]
            self.oe = OrdinalEncoder(categories=ord_data3)
            self.data_set[["Motivation_Level"]] = self.oe.fit_transform(
                self.data_set[["Motivation_Level"]])
            ord_data4 = [['Low', 'Medium', 'High']]
            self.oe = OrdinalEncoder(categories=ord_data4)
            self.data_set[["Family_Income"]] = self.oe.fit_transform(
                self.data_set[["Family_Income"]])
            ord_data5 = [['Low', 'Medium', 'High']]
            self.oe = OrdinalEncoder(categories=ord_data5)
            self.data_set[["Teacher_Quality"]] = self.oe.fit_transform(
                self.data_set[["Teacher_Quality"]])
            ord_data6 = [['Positive', 'Negative', 'Neutral']]
            self.oe = OrdinalEncoder(categories=ord_data6)
            self.data_set[["Peer_Influence"]] = self.oe.fit_transform(
                self.data_set[["Peer_Influence"]])
            ord_data7 = [['High School', 'College', 'Postgraduate']]
            self.oe = OrdinalEncoder(categories=ord_data7)
            self.data_set[["Parental_Education_Level"]] = self.oe.fit_transform(
                self.data_set[["Parental_Education_Level"]])
            ord_data8 = [['Near', 'Moderate', 'Far']]
            self.oe = OrdinalEncoder(categories=ord_data8)
            self.data_set[["Distance_from_Home"]] = self.oe.fit_transform(
                self.data_set[["Distance_from_Home"]])
            # performing onehot encoding in few colums in the dataset.
            en_data = self.data_set[['Extracurricular_Activities',
                                    'Internet_Access', 'School_Type', 'Learning_Disabilities', 'Gender']]

            array = self.ohe.fit_transform(en_data).toarray()

            self.data_set[['Extracurricular_Activities', 'Internet_Access', 'School_Type', 'Learning_Disabilities', 'Gender']] = pd.DataFrame(
                array, columns=['Extracurricular_Activities', 'Internet_Access', 'School_Type', 'Learning_Disabilities', 'Gender'])
            # Droping some more null values from row of the data set.
            self.data_set.dropna(inplace=True)

            self.data_set.to_sql(
                'student_performance_dataset',  # table name in PostgreSQL
                self.engine,
                if_exists='replace',    # 'replace' will drop table if exists, 'append' to add data
                index=False             # don't write DataFrame index as a column
            )
            logger.info("data set is save in to the postgrace succes fully")
            print("data set is save in to the postgrace succes fully")
        # producing kafka message.
            self.kafka_prodcer.produce(topic="mlpipeline", value=self.value)
            self.kafka_prodcer.flush()
            logger.info("producer produced event in the topic of the broker")
        except Exception as e:
            logger.error(f"there is an error ocurred{e}")
            raise RuntimeError({"Error": str(e)})
