def validate_record(row):

    if row["customer_id"].strip() == "":
        return "customer_id missing"

    if not row["customer_id"].isdigit():
        return "customer_id invalid"

    if row["amount"].strip() == "":
        return "amount missing"

    if float(row["amount"]) <= 0:
        return "invalid amount"

    if row["status"] not in ["completed","pending","cancelled"]:
        return "invalid status"

    return None