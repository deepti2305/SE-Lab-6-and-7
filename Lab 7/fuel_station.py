import math


def _to_float(value):
    """Convert value to a finite float, or return None if it is not possible."""
    try:
        if isinstance(value, bool):
            return None
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        return None
    return number if math.isfinite(number) else None


def parse_purchase(text):
    """Parse 'grade:litres' into (Grade, litres). Invalid input gives ('', 0.0)."""
    if not isinstance(text, str) or ":" not in text:
        return "", 0.0
    grade, litres_text = text.split(":", 1)
    litres = _to_float(litres_text)
    if litres is None or litres < 0:
        return "", 0.0
    return grade.strip().title(), litres


def volume_average(volumes_csv):
    """Average (floor) of the valid non-negative integer volumes. Invalid input gives 0."""
    if not isinstance(volumes_csv, str):
        return 0
    values = []
    for part in volumes_csv.split(","):
        try:
            number = int(part)
        except (ValueError, OverflowError):
            continue
        if number >= 0:
            values.append(number)
    if not values:
        return 0
    return sum(values) // len(values)


def payable_bill(text):
    """Bill * 1.18 - discount, never below 0. Invalid input gives 0.0."""
    if not isinstance(text, str) or "|" not in text:
        return 0.0
    bill_text, discount_text = text.split("|", 1)
    bill = _to_float(bill_text)
    discount = _to_float(discount_text)
    if bill is None or discount is None or bill < 0 or discount < 0:
        return 0.0
    total = bill * 1.18 - discount
    if not math.isfinite(total):
        return 0.0
    return max(total, 0.0)


def main():
    print("==== Running parse_purchase ====")
    user_input = input("Enter grade:litres (e.g. diesel:25): ")
    result = parse_purchase(user_input)
    print("Grade and Litres:", result)

    print("\n==== Running volume_average ====")
    user_input = input("Enter pump volumes in litres as CSV (e.g. 10,25,40): ")
    result = volume_average(user_input)
    print("Average Volume:", result)

    print("\n==== Running payable_bill ====")
    user_input = input("Enter bill|discount (e.g. 2500|100): ")
    result = payable_bill(user_input)
    print("Payable Bill:", result)

if __name__ == "__main__":
    main()
