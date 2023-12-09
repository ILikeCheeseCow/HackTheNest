import datetime
import json
import os
import logging
import time
import threading  # Import threading

# Constants
MEDICATION_FILE = "medications.json"
LOG_FILE = "medication_log.txt"

# Setup logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Function to load medications from file
def load_medications():
    if os.path.exists(MEDICATION_FILE):
        with open(MEDICATION_FILE, 'r') as file:
            return json.load(file)
    return {}

# Function to save medications to file
def save_medications(medications):
    with open(MEDICATION_FILE, 'w') as file:
        json.dump(medications, file, indent=4)

# Converts 24-hour time to 12-hour format with AM/PM
def format_time_12hr(hour, minute):
    hour = int(hour)
    minute = int(minute)
    am_pm = "AM" if hour < 12 else "PM"
    hour = hour % 12
    hour = 12 if hour == 0 else hour
    return f"{hour}:{minute:02d} {am_pm}"

# Simplified cron interpreter
def simple_cron_interpreter(cron_str):
    parts = cron_str.split()
    if len(parts) != 5:
        return "Invalid cron format"

    minutes, hours, day_of_month, month, day_of_week = parts

    readable = "Every "
    if minutes == "*" and hours == "*":
        readable += "minute"
    elif minutes == "0" and hours == "*":
        readable += "hour"
    elif minutes != "*" and hours != "*":
        readable += f"day at {format_time_12hr(hours, minutes)} "
    else:
        readable += "time not specific"

    return readable

# Function to add medication
def add_medication(medications, med_name, schedule):
    medications[med_name] = schedule
    save_medications(medications)
    logging.info(f"Added medication: {med_name} with schedule {schedule}")

# Function to remove medication
def remove_medication(medications, med_name):
    if med_name in medications:
        del medications[med_name]
        save_medications(medications)
        logging.info(f"Removed medication: {med_name}")

# Function to list medications in a human-readable format
def list_medications(medications):
    for med, schedule_str in medications.items():
        print(f"{med}: {simple_cron_interpreter(schedule_str)}")

# Function to check if it's time for medication
def check_for_meds(medications):
    current_time = datetime.datetime.now()
    for med, schedule_str in medications.items():
        minutes, hours, _, _, _ = schedule_str.split()
        scheduled_time = current_time.replace(hour=int(hours), minute=int(minutes), second=0, microsecond=0)

        if current_time.hour == scheduled_time.hour and current_time.minute == scheduled_time.minute:
            print(f"Time for meds: {med}")

# Function to run medication checks in a separate thread
def run_medication_checks(medications):
    while True:
        check_for_meds(medications)
        time.sleep(60)

# Main script
if __name__ == "__main__":
    medications = load_medications()

    # Start the medication check thread
    med_check_thread = threading.Thread(target=run_medication_checks, args=(medications,))
    med_check_thread.daemon = True
    med_check_thread.start()

    while True:
        print("\nMedication Scheduler")
        print("1. Add a medication")
        print("2. Remove a medication")
        print("3. List medications")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            med_name = input("Enter medication name: ")
            schedule = input("Enter schedule (in cron format, e.g., '0 10 * * *' for every day at 10 AM): ")
            add_medication(medications, med_name, schedule)
        elif choice == "2":
            med_name = input("Enter medication name to remove: ")
            remove_medication(medications, med_name)
        elif choice == "3":
            list_medications(medications)
        elif choice == "4":
            break
