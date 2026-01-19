# Exchange Rate Alert Notifier

## Get notified when it may be a good moment to exchange currency.

This Python application monitors foreign exchange rates and sends an SMS alert when a target currency reaches a user-defined threshold or experiences a significant drop in a short period of time. It has been
created to run automatically on a daily basis with the user's platform of choice.

### How it works

You define:
+ A base currency (the currency you hold)
+ A target currency (the currency you want to exchange into)
+ A target exchange rate

Then: 
1. The program fetches live exchange rates from the ExchangeRate API
2. Alerts are sent via Twilio SMS when conditions are met
3. A CSV log tracks historical exchange rates
4. A JSON state file ensures the confirmation message is sent only once

### Features

+ One-time SMS confirmation on first run
+ Periodic exchange-rate checks 
+ Alerts triggered by:
  + A target rate being reached 
  + A significant percentage drop within 30 days
+ Persistent state management using JSON
+ Lightweight CSV logging (no database required)

### Lessons learned

+ Initially, a pandas DataFrame was used to read the notification log. Since only the most recent exchange rate is needed, this was replaced with Python’s built-in csv.DictReader, reducing dependencies and improving performance.

+ Persistent state (JSON) is preferable to in-memory flags for preventing duplicate notifications in recurring or scheduled scripts.

+ Separating API access, notification logic, logging, and orchestration significantly improved maintainability and testability.

### Future improvements
+ Email notification option
+ Configurable alert direction (increase vs. decrease)