from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from pension import calculate_required_pot

app = FastAPI(title="Pension Plan API")
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"


class CalculateRequest(BaseModel):
    retirement_age: int = Field(..., ge=0)
    annual_real_return: float
    monthly_drawdown: float = Field(..., ge=0)
    death_age: int = Field(90, gt=0)


class CalculateResponse(BaseModel):
    required_pot_at_retirement: float
    note: str = ""


if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    index_path = STATIC_DIR / "index.html"
    if not index_path.exists():
        return HTMLResponse(
            "<h1>UI not built</h1><p>Build the Angular app to generate static files.</p>",
            status_code=503,
        )
    return HTMLResponse(index_path.read_text(encoding="utf-8"))


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
        note="",
    )
