from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PensionPlanResult:
    required_pot_now: float
    required_pot_at_retirement: float
    shortfall_now: float


def _calculate_monthly_effective_rate(annual_real_return_pcnt: float) -> float:
    if annual_real_return_pcnt <= -1:
        raise ValueError("annual_real_return must be greater than -1.0")
    return (1.0 + (annual_real_return_pcnt / 100)) ** (1.0 / 12.0) - 1.0


def _present_value_annuity(payment: float, monthly_rate: float, months: int) -> float:
    if months <= 0:
        raise ValueError("months must be positive")
    if monthly_rate == 0:
        return payment * months
    return payment * (1.0 - (1.0 + monthly_rate) ** (-months)) / monthly_rate


def calculate_required_pot(
    *,
    age_now: int,
    starting_balance: float,
    retirement_age: int,
    annual_real_return_pcnt: float,
    monthly_drawdown: float,
    death_age: int = 90,
) -> PensionPlanResult:
    """
    Calculate the required pension pot in 2026 (real) terms.

    All money values are treated as inflation-adjusted (real) amounts.
    """
    if age_now < 0 or retirement_age < 0 or death_age < 0:
        raise ValueError("ages must be non-negative")
    if retirement_age < age_now:
        raise ValueError("retirement_age must be >= age_now")
    if death_age <= retirement_age:
        raise ValueError("death_age must be > retirement_age")
    if starting_balance < 0:
        raise ValueError("starting_balance must be non-negative")
    if monthly_drawdown < 0:
        raise ValueError("monthly_drawdown must be non-negative")

    months_to_retirement = (retirement_age - age_now) * 12
    months_in_retirement = (death_age - retirement_age) * 12
    monthly_rate = _calculate_monthly_effective_rate(annual_real_return_pcnt)

    required_pot_at_retirement = _present_value_annuity(
        payment=monthly_drawdown,
        monthly_rate=monthly_rate,
        months=months_in_retirement,
    )

    if months_to_retirement == 0:
        required_pot_now = required_pot_at_retirement
    else:
        required_pot_now = required_pot_at_retirement / (1.0 + monthly_rate) ** months_to_retirement

    shortfall_now = max(0.0, required_pot_now - starting_balance)

    return PensionPlanResult(
        required_pot_now=required_pot_now,
        required_pot_at_retirement=required_pot_at_retirement,
        shortfall_now=shortfall_now,
    )
