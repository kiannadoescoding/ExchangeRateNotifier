import os
from twilio.rest import Client
from decimal import Decimal

from src.logger import LOG_FILE, append_log, read_last_log_entry

ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]

client = Client(ACCOUNT_SID, AUTH_TOKEN)

BASE_CURRENCY = os.getenv("BASE_CURRENCY")
TARGET_CURRENCY = os.getenv("TARGET_CURRENCY")
RATE_OF_INTEREST = Decimal(os.getenv('RATE_OF_INTEREST'))

def send_confirmation(current_rate: Decimal):
    confirmation = client.messages.create(
        body=f"You have signed up for currency exchange alerts. "
             f"You will be alerted when {TARGET_CURRENCY} is at or below {RATE_OF_INTEREST} of {BASE_CURRENCY}. "
             f"The current exchange rate is 1 {BASE_CURRENCY} to {current_rate} {TARGET_CURRENCY}",
        from_=os.environ['TWILIO_NUMBER'],
        to=os.environ['PHONE_NUMBER'],
    )
    return confirmation

def notify(alert_msg, current_rate, today):
    message = client.messages.create(
        body=f"{alert_msg}",
        from_=os.environ['TWILIO_NUMBER'],
        to=os.environ['PHONE_NUMBER'],
    )
    append_log(today,current_rate)
    return message

def check_alert_conditions(today, current_rate: Decimal):
    last_log_date, last_log_rate = read_last_log_entry(LOG_FILE)
    if last_log_date is None or last_log_rate is None:
        return

    delta = today - last_log_date
    days_since_last_log = delta.days
    percent_diff_since_last_log = (current_rate - last_log_rate)/last_log_rate * 100

    if days_since_last_log >= 30:
        if current_rate < RATE_OF_INTEREST:
            alert_msg = f'ALERT: The current {BASE_CURRENCY} exchange rate is ${current_rate}'
            notify(alert_msg,current_rate,today)
    else:
        if percent_diff_since_last_log <= -5:
            alert_msg = (f'ALERT: There has been a {percent_diff_since_last_log:.2f}% change in the '
                         f'current exchange rate from {BASE_CURRENCY} to {TARGET_CURRENCY}. The '
                         f'current rate is ${current_rate:.2f}')
            notify(alert_msg, current_rate, today)