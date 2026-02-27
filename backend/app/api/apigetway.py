import httpx
from fastapi import FastAPI
from ..router.serviceendpoint import dataframe_input

app = FastAPI()

PATH = "http://127.0.0.1:8002/api/v1/router_endpoint"


@app.post("/get_ouput")
async def model_output(data: dataframe_input):
    async with httpx.AsyncClient() as client:
        respones = await client.post(url=PATH, json=data.dict())
        return respones.json()
# uvicorn backend.app.api.apigetway:app --reload --port 8001
