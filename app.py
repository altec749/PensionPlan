from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from pension import calculate_required_pot

app = FastAPI(title="Pension Plan API")


class CalculateRequest(BaseModel):
    retirement_age: int = Field(..., ge=0)
    annual_real_return: float
    monthly_drawdown: float = Field(..., ge=0)
    death_age: int = Field(90, gt=0)


class CalculateResponse(BaseModel):
    required_pot_at_retirement: float
    note: str


@app.post("/calculate", response_model=CalculateResponse)
def calculate(request: CalculateRequest) -> CalculateResponse:
    try:
        result = calculate_required_pot(
            retirement_age=request.retirement_age,
            annual_real_return=request.annual_real_return,
            monthly_drawdown=request.monthly_drawdown,
            death_age=request.death_age,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return CalculateResponse(
        required_pot_at_retirement=result.required_pot_at_retirement,
        note="adam"
    )
