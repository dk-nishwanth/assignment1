import datetime
import time
import threading
import platform
import itertools
import sys
import os

def play_custom_sound():
    sound_path = "alarm.mp3"  # Change this to your file
    try:
        playsound(sound_path)
    except:
        print("Could not play sound. Make sure the file exists and is supported.")

def spinner_animation(stop_event):
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    while not stop_event.is_set():
        sys.stdout.write(f"\r⏳ Waiting {next(spinner)}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r✅ Reminder time reached!         \n')

def set_reminder(message, reminder_datetime):
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=spinner_animation, args=(stop_event,))
    spinner_thread.start()

    wait_seconds = (reminder_datetime - datetime.datetime.now()).total_seconds()
    if wait_seconds > 0:
        time.sleep(wait_seconds)

    stop_event.set()
    spinner_thread.join()
    
    print(f"\n🔔 Reminder: {message} (at {reminder_datetime.strftime('%H:%M')})")
    play_custom_sound()

def get_time_input():
    while True:
        time_format = input("Enter time format - 12 or 24 hour (type 12 or 24): ")
        if time_format == '12':
            reminder_time = input("Enter time (e.g., 02:30 PM): ")
            try:
                return datetime.datetime.strptime(reminder_time, "%I:%M %p")
            except ValueError:
                print("Invalid format. Try again (Example: 02:30 PM)")
        elif time_format == '24':
            reminder_time = input("Enter time (e.g., 14:30): ")
            try:
                return datetime.datetime.strptime(reminder_time, "%H:%M")
            except ValueError:
                print("Invalid format. Try again (Example: 14:30)")
        else:
            print("Please type either '12' or '24'.")

def remainder_bot():
    print("🎯 Welcome to the Animated Remainder Bot!")
    print("🕓 Current time:", datetime.datetime.now().strftime("%I:%M %p | %H:%M"))

    reminders = []
    while True:
        message = input("\n📝 What should I remind you about? ")
        reminder_time_input = get_time_input()

        now = datetime.datetime.now()
        reminder_datetime = now.replace(
            hour=reminder_time_input.hour,
            minute=reminder_time_input.minute,
            second=0,
            microsecond=0
        )

        if reminder_datetime < now:
            reminder_datetime += datetime.timedelta(days=1)

        reminders.append((message, reminder_datetime))

        more = input("➕ Add another reminder? (yes/no): ").strip().lower()
        if more != "yes":
            break

    print("\n✅ All reminders are set! Waiting...\n")
    for message, time_obj in reminders:
        threading.Thread(target=set_reminder, args=(message, time_obj)).start()

# Run the bot
remainder_bot()
