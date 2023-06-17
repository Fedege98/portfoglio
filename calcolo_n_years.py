import random
def calculate_investment(starting_amount, monthly_increase, annual_interest_rate, years):
    monthly_interest_rate = float(annual_interest_rate) / 12
    total_value = 0

    for year in range(1, years+1):
        monthly_deposit = starting_amount + ((year-1) * monthly_increase)
        for month in range(1, 13):
            total_value = (total_value + monthly_deposit) * (1 + monthly_interest_rate)
    return total_value

starting_amount = random.randrange(350,550)  # initial deposit amount
monthly_increase = random.randrange(100,200)  # increase in deposit every year
annual_interest_rate = random.randint(3, 5) / 100.0
 # 7% annual interest rate
years = 5  # number of years

total_value = calculate_investment(starting_amount, monthly_increase, annual_interest_rate, years)
print(f'The total value after {years} years is approximately {total_value:.2f} Euros.')
