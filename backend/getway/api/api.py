from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

MODEL_SERVICE_URL = "http://127.0.0.1:8001/model_service_api_server/predict"


# Global async client
client: httpx.AsyncClient = None


# ---------------- STARTUP ----------------

@app.on_event("startup")
async def startup_event():
    global client
    client = httpx.AsyncClient(timeout=10.0)


# ---------------- SHUTDOWN ----------------

@app.on_event("shutdown")
async def shutdown_event():
    await client.aclose()


# ---------------- ROUTE ----------------

@app.post("/predict")
async def gateway_predict(data: dict):

    try:
        response = await client.post(
            MODEL_SERVICE_URL,
            json=data
        )

        response.raise_for_status()

        return response.json()

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Model service unavailable"
        )

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Model service error: {e.response.text}"
        )
