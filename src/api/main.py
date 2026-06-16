from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from predictor import predictor

app = FastAPI(
    title="Retail Demand Forecasting API",
    description="Forecasts daily unit sales using a trained LightGBM model",
    version="1.0.0"
)


class ForecastRequest(BaseModel):
    item_id: str
    horizon: int = 28


class ForecastDay(BaseModel):
    date: str
    predicted_sales: float


class ForecastResponse(BaseModel):
    item_id: str
    horizon: int
    forecast: List[ForecastDay]


@app.get("/")
def root():
    return {
        "message": "Retail Demand Forecasting API",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/items")
def get_items():
    items = predictor.get_available_items()

    return {
        "count": len(items),
        "items": items[:20],
        "note": "showing first 20 items"
    }


@app.post("/forecast", response_model=ForecastResponse)
def forecast(request: ForecastRequest):

    try:
        if request.horizon < 1 or request.horizon > 90:
            raise HTTPException(
                status_code=400,
                detail="horizon must be between 1 and 90"
            )

        result = predictor.predict(
            request.item_id,
            request.horizon
        )

        return {
            "item_id": request.item_id,
            "horizon": request.horizon,
            "forecast": result
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )