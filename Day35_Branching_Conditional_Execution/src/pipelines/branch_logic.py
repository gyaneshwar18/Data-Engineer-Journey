def choose_path():
    records = 10

    if records > 0:
        return "process_data"

    return "send_alert"


def process_data():
    print("Processing records...")


def send_alert():
    print("No records found. Alert sent.")
