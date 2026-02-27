from pydantic import BaseModel
from typing import Literal
from fastapi import APIRouter
from fastapi import FastAPI
from ..services.modelservice import ModelService


class dataframe_input(BaseModel):
    Hours_Studied: int
    Attendance: int
    Parental_Involvement: Literal["low", "Midium", "High"]
    Access_to_Resources: Literal["low", "Midium", "High"]
    Extracurricular_Activities: Literal["Yes", "No"]
    Sleep_Hours: int
    Previous_Scores: int
    Motivation_Level: Literal["low", "Midium", "High"]
    Internet_Access: Literal["Yes", "No"]
    Tutoring_Sessions: int
    Family_Income: Literal["low", "Midium", "High"]
    Teacher_Quality: Literal["low", "Midium", "High"]
    School_Type:  Literal["Private", "Public"]
    Peer_Influence: Literal["Positive", "Negative", "Neutral"]
    Physical_Activity: int
    Learning_Disabilities: Literal["Yes", "No"]
    Parental_Education_Level: Literal["High School",
                                      "Collage", "Postgraduate"]
    Distance_from_Home: Literal["Near", "Moderate", "Far"]
    Gender: Literal["Male", "Female"]


router = APIRouter()
service = ModelService()
app = FastAPI()


@router.post("/router_endpoint")
def input_data(input: dict) -> float:
    output = service.predict(input)
    return output
