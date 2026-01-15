from pension import calculate_required_pot


def main() -> None:

    target_monthly_drawdown=3725.0

    print(f"Target monthly (pre-tax): {target_monthly_drawdown:,.2f}")

    result = calculate_required_pot(
        retirement_age=60,
        annual_real_return=0.04,
        monthly_drawdown=target_monthly_drawdown,
        death_age=100,
    )

    print(f"Required pot at retirement: {result.required_pot_at_retirement:,.2f}")


if __name__ == "__main__":
    main()
