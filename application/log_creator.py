from random import choice, randint, uniform
from time import sleep
from string import ascii_letters
from glob import glob

LOG_FILE = "./server.log"
LOG_LEVELS = ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]


def generate_log_entry():
    log_level = choice(LOG_LEVELS)
    day = randint(1, 28)
    month = randint(6, 7)
    year = 2024
    hour = randint(0, 23)
    minute = randint(0, 59)
    second = randint(0, 59)
    current_time = f'{year}-{"0" if month < 10 else "" }{month}-{"0" if day < 10 else "" }{day} {"0" if hour < 10 else "" }{hour}:{"0" if minute < 10 else "" }{minute}:{"0" if second < 10 else "" }{second},{randint(100,999)}'
    N = randint(1, 400)
    random_message = "".join(choice(ascii_letters) for _ in range(N))
    log_entry = f"{log_level} {current_time} {random_message}\n"
    return log_entry


def update_log_file(log_file):
    if not glob(log_file):
        with open(log_file, "w") as f:
            log_entry = generate_log_entry()
            f.write(log_entry)
            # print("server.log file created")
            # print(f"Added log entry: {log_entry.strip()}")
    with open(log_file, "a") as f:
        log_entry = generate_log_entry()
        f.write(log_entry)
        # print(f"Added log entry: {log_entry.strip()}")


if __name__ == "__main__":
    while True:
        update_log_file(LOG_FILE)
        sleep(uniform(0.001, 0.002))
