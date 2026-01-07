import math

import pytest

from pension import calculate_required_pot
from pension import _calculate_monthly_effective_rate


def test_zero_return_one_year_retirement() -> None:
    result = calculate_required_pot(
        age_now=60,
        starting_balance=0.0,
        retirement_age=60,
        annual_real_return_pcnt=0.0,
        monthly_drawdown=1000.0,
        death_age=61,
    )

    assert result.required_pot_now == pytest.approx(12_000.0)
    assert result.required_pot_at_retirement == pytest.approx(12_000.0)
    assert result.shortfall_now == pytest.approx(12_000.0)


def test_positive_return_matches_annuity_formula() -> None:
    monthly_rate = 0.01
    annual_real_return = (1.0 + monthly_rate) ** 12 - 1.0

    result = calculate_required_pot(
        age_now=60,
        starting_balance=0.0,
        retirement_age=60,
        annual_real_return_pcnt=annual_real_return,
        monthly_drawdown=500.0,
        death_age=62,
    )

    months = 24
    expected = 500.0 * (1.0 - (1.0 + monthly_rate) ** (-months)) / monthly_rate

    assert result.required_pot_now == pytest.approx(expected)
    assert result.required_pot_at_retirement == pytest.approx(expected)


def test_discounting_back_to_today() -> None:
    result = calculate_required_pot(
        age_now=50,
        starting_balance=0.0,
        retirement_age=60,
        annual_real_return_pcnt=0.05,
        monthly_drawdown=1000.0,
        death_age=61,
    )

    monthly_rate = (1.0 + 0.05) ** (1.0 / 12.0) - 1.0
    required_at_retirement = 1000.0 * 12
    expected_now = required_at_retirement / (1.0 + monthly_rate) ** (10 * 12)

    assert math.isclose(result.required_pot_now, expected_now, rel_tol=1e-10)

def test_monthly_rate_calc() -> None:
    expected = 0.3273739 / 100
    result = _calculate_monthly_effective_rate(4)

    assert math.isclose(result, expected, rel_tol=1e-5)

def test_invalid_inputs() -> None:
    with pytest.raises(ValueError, match="retirement_age must be >= age_now"):
        calculate_required_pot(
            age_now=65,
            starting_balance=0.0,
            retirement_age=60,
            annual_real_return_pcnt=0.02,
            monthly_drawdown=1000.0,
            death_age=90,
        )
