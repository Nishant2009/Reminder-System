import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from twilio.rest import Client

# Twilio credentials (replace with your actual credentials)
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = 'whatsapp:+1234567890'

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# In-memory storage for reminders and opt-outs
reminders: List[Dict] = []
opt_out_users: set = set()
recurring_reminders: List[Dict] = []

async def add_reminder(user_id: str, phone: str, message: str, remind_at: datetime, tz: str = 'UTC', whatsapp: bool = True, recurring: Optional[str] = None):
    """
    Store a reminder asynchronously.
    """
    reminder = {
        'user_id': user_id,
        'phone': phone,
        'message': message,
        'remind_at': remind_at,
        'tz': tz,
        'whatsapp': whatsapp,
        'recurring': recurring
    }
    reminders.append(reminder)
    if recurring:
        recurring_reminders.append(reminder)
    print(f"Reminder added for {user_id} at {remind_at} {tz}")

async def opt_out(user_id: str):
    opt_out_users.add(user_id)
    print(f"User {user_id} opted out.")

async def send_reminder(reminder: Dict):
    if reminder['user_id'] in opt_out_users:
        print(f"User {reminder['user_id']} opted out. Skipping.")
        return
    to = reminder['phone']
    body = reminder['message']
    if reminder['whatsapp']:
        to = f"whatsapp:{to}"
    try:
        client.messages.create(
            body=body,
            from_=TWILIO_PHONE_NUMBER,
            to=to
        )
        print(f"Sent reminder to {to}: {body}")
    except Exception as e:
        print(f"Failed to send reminder to {to}: {e}")

async def check_and_send_reminders():
    now_utc = datetime.utcnow().replace(tzinfo=pytz.UTC)
    to_send = []
    for reminder in reminders[:]:
        remind_at = reminder['remind_at']
        tz = pytz.timezone(reminder['tz'])
        remind_at_local = tz.localize(remind_at)
        remind_at_utc = remind_at_local.astimezone(pytz.UTC)
        if now_utc >= remind_at_utc:
            to_send.append(reminder)
            reminders.remove(reminder)
            # Handle recurring
            if reminder.get('recurring'):
                next_time = get_next_recurring(remind_at_local, reminder['recurring'])
                if next_time:
                    await add_reminder(
                        reminder['user_id'], reminder['phone'], reminder['message'],
                        next_time.replace(tzinfo=None), reminder['tz'], reminder['whatsapp'], reminder['recurring']
                    )
    for reminder in to_send:
        await send_reminder(reminder)

def get_next_recurring(current: datetime, recurring: str) -> Optional[datetime]:
    if recurring == 'daily':
        return current + timedelta(days=1)
    elif recurring == 'weekly':
        return current + timedelta(weeks=1)
    elif recurring == 'hourly':
        return current + timedelta(hours=1)
    return None

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_and_send_reminders, 'interval', seconds=30)
    scheduler.start()
    print("Scheduler started.")

async def main():
    start_scheduler()

    # Example usage
    await add_reminder(
        user_id='user1',
        phone='+911234567890',
        message='Test WhatsApp reminder!',
        remind_at=datetime.now() + timedelta(seconds=10),  # Set to 10 seconds from now
        tz='Asia/Kolkata',
        whatsapp=True,
        recurring='daily'
    )
    await asyncio.sleep(180) # Keep the script running for 3 minutes

if __name__ == "__main__":
    asyncio.run(main())
