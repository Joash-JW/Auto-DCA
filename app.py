from td import TD
from ibkr import IBKR
from moomoo import MooMoo
from tiger import Tiger
from datetime import datetime, timedelta
from pytz import timezone, utc
from requests import get
from threading import Timer
from dateutil.relativedelta import relativedelta


market_timezone = timezone('US/Eastern')  # Timezone of US Stock Market


def get_user_broker():
    # Keep prompting user to input choice until valid input is received.
    # Valid input is a number from 1 to 4.
    while True:
        try:
            choice = int(input(
                "Please choose your broker:\n"
                "1. TD Ameritrade\n"
                "2. Interactive Brokers\n"
                "3. Moomoo\n"
                "4. Tiger\n"))
            assert 1 <= choice <= 4
            break  # break when valid input received
        except (ValueError, AssertionError):
            print("Please input a number from 1 to 4\n")

    # Map user choice to respective brokers.
    if choice == 1:
        broker = TD()
    elif choice == 2:
        broker = IBKR()
    elif choice == 3:
        broker = MooMoo()
    else:
        broker = Tiger()

    print("Choice of broker selected: " + broker.name, end='\n\n')

    return broker


def get_user_dca_date():
    # Keep prompting user until valid input is received.
    # Valid input must fulfill these criteria
    # 1. In right format, YYYY-mm-dd HH:MM
    # 2. Cannot be in the past.
    # 3. Within US Market opening hours.
    while True:
        try:
            datetime_choice = str(input("Enter your next DCA date and time (EST timezone) in "
                                        "YYYY-mm-dd HH:MM format (e.g. 2022-1-29 11:00):\n"))
            dca_date = datetime.strptime(datetime_choice, "%Y-%m-%d %H:%M")

            # This step is so that arithmetic on datetime that cross DST boundaries will be consistent.
            dca_date = market_timezone.normalize(market_timezone.localize(dca_date))

            assert datetime.now(tz=market_timezone) < dca_date  # Input must be in the future

            market_start = datetime(year=dca_date.year, month=dca_date.month, day=dca_date.day,
                                    hour=9, minute=30)
            market_start = market_timezone.normalize(market_timezone.localize(market_start))  # Make consistent

            market_end = datetime(year=dca_date.year, month=dca_date.month, day=dca_date.day,
                                  hour=16, minute=00)
            market_end = market_timezone.normalize(market_timezone.localize(market_end))  # Make consistent

            assert market_start <= dca_date <= market_end  # Input must be in within market opening hours

            print("DCA date selected: " + dca_date.strftime("%Y-%m-%d %H:%M:%S"))
            return dca_date  # exit when valid input received
        except (ValueError, AssertionError):
            print("Please ensure your input is in the right format, not in the past and "
                  "within US Market opening hours 9.30am-4.00pm\n")


def adjust_dca_date(dca_date):
    # Loop to tackle edge case - DCA date falls in last day of the month and market is closed. (e.g 2022-04-30)
    # It will proceed to query calendar information for the following month.
    while True:
        market_calendar = query_us_market_calendar(dca_date.year, dca_date.month)

        # Simple loop to check whether market is open on the date.
        for date_info in market_calendar['days']['day']:
            if date_info['date'] == dca_date.strftime("%Y-%m-%d"):
                if date_info['status'] == 'open':
                    return dca_date

                # Set DCA date to next day and check status of the market for that day.
                dca_date += timedelta(days=1)


def query_us_market_calendar(year, month):
    # Query US market calendar information.
    while True:
        try:
            print("Querying US market calendar date for year={year}, month={month}".format(year=year, month=month))
            response = get(
                'https://api.tradier.com/v1/markets/calendar',
                params={'month': str(month), 'year': str(year)},
                headers={'Authorization': 'Bearer <TOKEN>', 'Accept': 'application/json'}
            )
            assert response.status_code == 200  # Try again if unable to get calendar information
            return response.json()['calendar']
        except AssertionError:
            print("Unable to get US market calendar")


def do_dca_wrapper(broker, dca_date):
    broker.do_dca()

    # Compute next DCA date
    next_dca_date = dca_date + relativedelta(months=1)
    next_dca_date = adjust_dca_date(next_dca_date)
    print("Next DCA Date after adjustment: " + next_dca_date.strftime("%Y-%m-%d %H:%M:%S"))
    delay = (next_dca_date - market_timezone.normalize((datetime.now(tz=utc)))).total_seconds()
    Timer(delay, do_dca_wrapper, args=(broker, next_dca_date)).start()  # Schedule next DCA
    print("DCA Completed for {dca_date}".format(dca_date=dca_date.strftime("%Y-%m-%d %H:%M:%S")))


if __name__ == '__main__':
    print("This app helps to automate your MONTHLY Dollar-Cost Averaging (DCA)\n")
    user_broker = get_user_broker()
    user_dca_date = get_user_dca_date()
    user_dca_date = adjust_dca_date(user_dca_date)
    print("DCA Date after adjustment: " + user_dca_date.strftime("%Y-%m-%d %H:%M:%S"))

    # Calculate time difference in seconds to DCA date
    seconds_to_delay = (user_dca_date - market_timezone.normalize((datetime.now(tz=utc)))).total_seconds()
    Timer(seconds_to_delay, do_dca_wrapper, args=(user_broker, user_dca_date)).start()  # Schedule DCA after delay
