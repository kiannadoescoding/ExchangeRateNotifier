from pathlib import Path
import json
from datetime import datetime

from src.api import get_exchange_rate
from src.logger import initialize_log
from src.notifier import check_alert_conditions, send_confirmation

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
STATE_FILE = DATA_DIR / "state.json"

def main():
    today = datetime.today().date()
    current_rate = get_exchange_rate()

    if not STATE_FILE.is_file():
        send_confirmation(current_rate)
        with open(STATE_FILE,'w') as f:
            data = {"confirmation_sent": True}
            json.dump(data,f)

    check_alert_conditions(today,current_rate)
    initialize_log(today,current_rate)

if __name__ == '__main__':
    main()