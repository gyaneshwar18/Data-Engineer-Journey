from datetime import datetime

VALID_STATUS = ["completed", "pending", "cancelled"]

def validate_record(row):

    if not row["customer_id"]:
        return "Missing customer_id"

    try:
        amount = float(row["amount"])
        if amount <= 0:
            return "Invalid amount"
    except:
        return "Amount not numeric"

    try:
        datetime.strptime(row["order_date"], "%Y-%m-%d")
    except:
        return "Invalid date format"

    if row["status"] not in VALID_STATUS:
        return "Invalid status"

    return None