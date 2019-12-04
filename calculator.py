from calendar import monthrange
import configargparse
from typing import Tuple

p = configargparse.ArgParser()
p.add('--loan', required=True, type=float, help='original loan amount')
p.add('--apr', required=True, type=float, help='Annual Percentage Rate; if 4%, put 4.0')
p.add('--length', required=True, type=int, help='Length of loan, in months')
p.add('--required_payment', required=True, type=float, help='Required payment per month')
p.add('--extra_payment', required=True, type=float, help='Extra payment per month')
p.add('--start_year', required=True, type=int, help='Year as an integer')
p.add('--start_month', required=True, type=int, help='Month as an integer')

def get_daily_rate(loan, apr):

    daily_rate = apr / 365.0
    return loan * daily_rate / 100

def get_monthly_rate(loan: float, apr: float, month: Tuple[int, int]):

    '''

    :param loan: Loan amount at the beginning of the month
    :param apr: Annual percentage rate
    :param month: Year and month respectively. E.g December 2019 is (2019, 12)
    :return:
    '''

    _, n_days = monthrange(month[0], month[1])
    return get_daily_rate(loan, apr) * n_days

def get_total_interest(loan: float,
                       apr: float,
                       length: int,
                       monthly_payment: float,
                       extra_monthly_payment: float,
                       month: Tuple[int, int],
                       interests=list()):

    if loan < 0 or length == 0:
        return interests

    total_payment = monthly_payment + extra_monthly_payment
    monthly_interest = get_monthly_rate(loan, apr, month)
    towards_principal = total_payment - monthly_interest
    unpaid_principal = loan - towards_principal

    interests.append(monthly_interest)

    if month[1] == 12:
        month = (month[0]+1, 1)
    else:
        month = (month[0], month[1]+1)

    return get_total_interest(unpaid_principal,
                              apr,
                              length - 1,
                              monthly_payment,
                              extra_monthly_payment,
                              month,
                              interests)

def main(args):
    loan = args.loan
    apr = args.apr
    length = args.length
    monthly = args.required_payment
    extra = args.extra_payment
    initial_month = (args.start_year, args.start_month)

    interests = get_total_interest(loan, apr, length, monthly, extra, initial_month, list())
    print(f"Taking {len(interests)} months to pay")
    print(f"Paying {sum(interests)} dollars in interest")
    print(interests)

if __name__ == "__main__":
    args = p.parse_args()
    main(args)








