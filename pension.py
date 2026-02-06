from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PensionPlanResult:
    required_pot_at_retirement: float


@dataclass(frozen=True)
class AnnualContributionResult:
    required_annual_contribution: float


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


def calculate_required_annual_contribution(
    *,
    target_pot: float,
    starting_pot: float,
    years_until_retirement: int,
    annual_real_return: float = 0.0,
) -> AnnualContributionResult:
    """
    Calculate the required annual contribution in real terms to hit a target pot.

    Contributions are assumed to be made at the end of each year.
    """
    if years_until_retirement <= 0:
        raise ValueError("years_until_retirement must be positive")
    if target_pot < 0:
        raise ValueError("target_pot must be non-negative")
    if starting_pot < 0:
        raise ValueError("starting_pot must be non-negative")
    if annual_real_return <= -1:
        raise ValueError("annual_real_return must be greater than -1.0")

    growth_factor = (1.0 + annual_real_return) ** years_until_retirement
    target_gap = target_pot - starting_pot * growth_factor

    if target_gap <= 0:
        required_annual_contribution = 0.0
    elif annual_real_return == 0:
        required_annual_contribution = target_gap / years_until_retirement
    else:
        required_annual_contribution = (
            target_gap * annual_real_return / (growth_factor - 1.0)
        )

    return AnnualContributionResult(
        required_annual_contribution=required_annual_contribution
    )
