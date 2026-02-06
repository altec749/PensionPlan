from pathlib import Path

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from pension import calculate_required_annual_contribution
from pension import calculate_required_pot

app = FastAPI(title="Pension Plan API")
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CalculateRequest(BaseModel):
    retirement_age: int = Field(..., ge=0)
    annual_real_return: float
    monthly_drawdown: float = Field(..., ge=0)
    death_age: int = Field(90, gt=0)


class CalculateResponse(BaseModel):
    required_pot_at_retirement: float
    note: str = ""


class AnnualContributionRequest(BaseModel):
    target_pot: float = Field(..., ge=0)
    starting_pot: float = Field(..., ge=0)
    years_until_retirement: int = Field(..., gt=0)
    annual_real_return: float = 0.0


class AnnualContributionResponse(BaseModel):
    required_annual_contribution: float
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


@app.post("/calculate-annual-contribution", response_model=AnnualContributionResponse)
def calculate_annual_contribution(
    request: AnnualContributionRequest,
) -> AnnualContributionResponse:
    try:
        result = calculate_required_annual_contribution(
            target_pot=request.target_pot,
            starting_pot=request.starting_pot,
            years_until_retirement=request.years_until_retirement,
            annual_real_return=request.annual_real_return,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return AnnualContributionResponse(
        required_annual_contribution=result.required_annual_contribution,
        note="",
    )


@app.options("/calculate")
def calculate_options() -> Response:
    return Response(status_code=200)


@app.options("/calculate-annual-contribution")
def calculate_annual_contribution_options() -> Response:
    return Response(status_code=200)
