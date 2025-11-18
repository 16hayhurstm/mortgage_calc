def simulate_mortgage(
    principal,
    daily_interest,
    monthly_payment,
    extra_payment=0,
    max_years=50,
    days_per_month=30,
):
    

    balance = float(principal)
    total_interest = 0.0
    total_paid = 0.0

    payoff_year = None
    payoff_month = None
    months_elapsed = 0

    for year in range(max_years):
        for month in range(12):
            for day in range(days_per_month):
                # interest daily
                interest_today = balance * daily_interest
                balance += interest_today
                total_interest += interest_today

                # extra payment halfway through the month
                if day == days_per_month // 2 and extra_payment > 0 and balance > 0:
                    payment = min(extra_payment, balance)
                    balance -= payment
                    total_paid += payment

                    if balance <= 0:
                        payoff_year = year + 1
                        payoff_month = month + 1
                        months_elapsed = year * 12 + month + 1
                        return {
                            "payoff_year": payoff_year,
                            "payoff_month": payoff_month,
                            "months_elapsed": months_elapsed,
                            "total_interest": total_interest,
                            "total_paid": total_paid,
                            "remaining_balance": 0.0,
                        }

            # normal monthly payment at end of month
            if balance > 0:
                payment = min(monthly_payment, balance)
                balance -= payment
                total_paid += payment

            months_elapsed += 1

            if balance <= 0:
                payoff_year = year + 1
                payoff_month = month + 1
                return {
                    "payoff_year": payoff_year,
                    "payoff_month": payoff_month,
                    "months_elapsed": months_elapsed,
                    "total_interest": total_interest,
                    "total_paid": total_paid,
                    "remaining_balance": 0.0,
                }

    # not fully paid within max_years
    return {
        "payoff_year": None,
        "payoff_month": None,
        "months_elapsed": months_elapsed,
        "total_interest": total_interest,
        "total_paid": total_paid,
        "remaining_balance": balance,
    }


# Example use

principal = 140000
daily_interest = 0.05 / 365  
monthly_payment = 900

base = simulate_mortgage(principal, daily_interest, monthly_payment, extra_payment=0)
overpay = simulate_mortgage(principal, daily_interest, monthly_payment, extra_payment=100)

print("No extra payment:")
print(base)

print("\nExtra £200 monthly:")
print(overpay)

if base["payoff_year"] and overpay["payoff_year"]:
    months_saved = base["months_elapsed"] - overpay["months_elapsed"]
    interest_saved = base["total_interest"] - overpay["total_interest"]
    print(f"\nMonths saved by overpaying: {months_saved}")
    print(f"Interest saved by overpaying: £{interest_saved:,.2f}")
