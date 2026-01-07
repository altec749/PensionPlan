from pension import calculate_required_pot


def main() -> None:
    result = calculate_required_pot(
        age_now=45,
        starting_balance=120000.0,
        retirement_age=67,
        annual_real_return_pcnt=0.03,
        monthly_drawdown=2500.0,
        death_age=90,
    )

    print(f"Required pot now: {result.required_pot_now:,.2f}")
    print(f"Required pot at retirement: {result.required_pot_at_retirement:,.2f}")
    print(f"Shortfall now: {result.shortfall_now:,.2f}")


if __name__ == "__main__":
    main()
