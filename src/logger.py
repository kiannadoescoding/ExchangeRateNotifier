import os
import csv
from pathlib import Path
from decimal import Decimal
from datetime import datetime

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
LOG_FILE = DATA_DIR / "notification_log.csv"

TARGET_CURRENCY = os.getenv("TARGET_CURRENCY")

def initialize_log(today, current_target_rate: Decimal):
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True)

    if not LOG_FILE.is_file():
        with open(LOG_FILE, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            field = ["date", TARGET_CURRENCY]
            writer.writerow(field)
            writer.writerow([today,current_target_rate])

def append_log(today,current_rate: Decimal):
    with open(LOG_FILE, 'a', newline='') as csvfile:
        add = csv.writer(csvfile)
        add.writerow([today, current_rate])

def read_last_log_entry(LOG_FILE):
    last_row = None
    if not LOG_FILE.is_file():
        return None, None

    with open(LOG_FILE, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            last_row = row
        if not last_row:
            return None, None
        return (
            datetime.strptime(last_row['date'],"%Y-%m-%d").date(), Decimal(last_row[TARGET_CURRENCY])
            )