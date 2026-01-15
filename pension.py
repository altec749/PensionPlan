from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PensionPlanResult:
    required_pot_at_retirement: float


def _calculate_monthly_effective_rate(annual_real_return: float) -> float:
    if annual_real_return <= -1:
        raise ValueError("annual_real_return must be greater than -1.0")
    return (1.0 + (annual_real_return)) ** (1.0 / 12.0) - 1.0


def _present_value_annuity(payment: float, monthly_rate: float, months: int) -> float:
    if months <= 0:
        raise ValueError("months must be positive")
    if monthly_rate == 0:
        return payment * months
    return payment * (1.0 - (1.0 + monthly_rate) ** (-months)) / monthly_rate


def calculate_required_pot(
    *,
    retirement_age: int,
    annual_real_return: float,
    monthly_drawdown: float,
    death_age: int = 90,
) -> PensionPlanResult:
    """
    Calculate the required pension pot in 2026 (real) terms.

    All money values are treated as inflation-adjusted (real) amounts.
    """
    if death_age <= retirement_age:
        raise ValueError("death_age must be > retirement_age")
    if monthly_drawdown < 0:
        raise ValueError("monthly_drawdown must be non-negative")

    months_in_retirement = (death_age - retirement_age) * 12
    monthly_rate = _calculate_monthly_effective_rate(annual_real_return)

    required_pot_at_retirement = _present_value_annuity(
        payment=monthly_drawdown,
        monthly_rate=monthly_rate,
        months=months_in_retirement,
    )

    return PensionPlanResult(
        required_pot_at_retirement=required_pot_at_retirement
    )
