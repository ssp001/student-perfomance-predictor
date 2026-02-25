import joblib
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
import numpy as np
import pandas as pd


class Model_Service:
    def __init__(self):
        self.model = joblib.load(
            "backend/model_service/model/model_predictor.pkl")
        # IMPORTANT: must match training order
        self.ordinal_structure = {
            "Parental_Involvement": ['Low', 'Medium', 'High'],
            "Access_to_Resources": ['Low', 'Medium', 'High'],
            "Motivation_Level": ['Low', 'Medium', 'High'],
            "Family_Income": ['Low', 'Medium', 'High'],
            "Teacher_Quality": ['Low', 'Medium', 'High'],
            "Peer_Influence": ['Negative', 'Neutral', 'Positive'],
            "Parental_Education_Level": ['High School', 'College', 'Postgraduate'],
            "Distance_from_Home": ['Near', 'Moderate', 'Far']
        }

        self.onehot_columns = [
            'Extracurricular_Activities',
            'Internet_Access',
            'School_Type',
            'Learning_Disabilities',
            'Gender'
        ]

        self.numeric_columns = [
            "Hours_Studied",
            "Attendance",
            "Sleep_Hours",
            "Previous_Scores",
            "Tutoring_Sessions",
            "Physical_Activity"
        ]

    # ---------------- ENCODING ----------------

    def encode_input(self, user_input: dict) -> np.ndarray:

        df = pd.DataFrame([user_input])

        # ----- Ordinal Encoding -----
        for column, categories in self.ordinal_structure.items():
            encoder = OrdinalEncoder(categories=[categories])
            df[[column]] = encoder.fit_transform(df[[column]])

        # ----- OneHot Encoding -----
        ohe = OneHotEncoder(drop="first", sparse=False)
        ohe_array = ohe.fit_transform(df[self.onehot_columns])

        ohe_df = pd.DataFrame(
            ohe_array,
            columns=ohe.get_feature_names_out(self.onehot_columns)
        )

        df = df.drop(columns=self.onehot_columns)
        df = pd.concat([df.reset_index(drop=True),
                        ohe_df.reset_index(drop=True)], axis=1)

        return df.values

    # ---------------- PREDICT ----------------

    def predict(self, user_input: dict) -> float:

        encoded_data = self.encode_input(user_input)

        prediction = self.model.predict(encoded_data)

        return float(prediction[0])
