import os
import requests
from dotenv import load_dotenv
from decimal import Decimal, ROUND_HALF_UP

load_dotenv()

EXC_RATE_API_KEY = os.getenv("ER_API_KEY")
BASE_CURRENCY = os.getenv("BASE_CURRENCY")
TARGET_CURRENCY = os.getenv("TARGET_CURRENCY")

def get_exchange_rate():
    if not EXC_RATE_API_KEY:
        raise EnvironmentError("Missing ER_API_KEY")
    url = f'https://v6.exchangerate-api.com/v6/{EXC_RATE_API_KEY}/latest/{BASE_CURRENCY}'

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        all_rates = data["conversion_rates"]
        current_rate = Decimal(str(all_rates[TARGET_CURRENCY])).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP)
        return current_rate

    except requests.RequestException as e:
        raise RuntimeError(f"Exchange rate API failed: {e}")


