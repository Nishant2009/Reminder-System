# User Reminder System with Background Cron Job (Twilio WhatsApp Integration)

## Overview
This project is a Python-based reminder service that sends scheduled WhatsApp messages to users using Twilio. Reminders are stored in memory and dispatched by a background cron-like job. The system supports timezones, opt-outs, and recurring reminders.

## Features
- Async capture and storage of reminders
- Background scheduler (APScheduler) for sending reminders
- Twilio WhatsApp integration
- Timezone-aware scheduling
- User opt-out support
- Recurring reminders (daily, weekly, hourly)

## Requirements
- Python 3.10+
- Twilio account with WhatsApp sandbox enabled
- The following Python packages:
  - twilio
  - apscheduler
  - pytz

## Setup
1. **Clone the repository or copy the files to your project folder.**
2. **Create and activate a Python virtual environment:**
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```powershell
   pip install twilio apscheduler pytz
   ```
4. **Configure Twilio credentials in `reminder_service.py`:**
   - `TWILIO_ACCOUNT_SID`: Your Twilio Account SID
   - `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token
   - `TWILIO_PHONE_NUMBER`: Your Twilio WhatsApp sandbox number, e.g., `whatsapp:+14155238886`

## WhatsApp Sandbox Setup
1. Go to [Twilio Console > Messaging > Try it Out > Send a WhatsApp message](https://www.twilio.com/console/sms/whatsapp/sandbox).
2. Send the join code from your WhatsApp to the Twilio sandbox number.
3. Use your WhatsApp-enabled number in E.164 format (e.g., `+919306920288`).

## Usage
1. **Run the service:**
   ```powershell
   python reminder_service.py
   ```
2. The script will schedule a test WhatsApp reminder 10 seconds from startup. You can modify or extend the logic in `main()` to add more reminders.

## Example Reminder
```python
await add_reminder(
    user_id='user1',
    phone='+919306920288',
    message='Test WhatsApp reminder!',
    remind_at=datetime.now() + timedelta(seconds=10),
    tz='Asia/Kolkata',
    whatsapp=True,
    recurring=None
)
```

## Troubleshooting
- Ensure your Twilio credentials and WhatsApp sandbox number are correct.
- The recipient must join the Twilio WhatsApp sandbox before receiving messages.
- Use the correct sender format: `whatsapp:+14155238886`.
- Check the terminal for error messages if reminders are not sent.

## License
MIT License
