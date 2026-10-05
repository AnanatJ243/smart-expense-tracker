from datetime import datetime

CATEGORIES = ["Food","Travel","Rent","Entertainment","Shopping","Bills","Health","Education","Other"]
PAYMENT_MODES = ["Cash","UPI","Card","Bank Transfer","Other"]

def parse_date(value: str):
    try: return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except ValueError as exc: raise ValueError("Date must use YYYY-MM-DD format.") from exc

def positive_amount(value: str) -> float:
    try: amount = float(value)
    except ValueError as exc: raise ValueError("Amount must be a valid number.") from exc
    if amount <= 0: raise ValueError("Amount must be greater than zero.")
    return round(amount, 2)

def valid_category(value: str) -> str:
    value = value.strip().title()
    if value not in CATEGORIES: raise ValueError(f"Unknown category. Choose: {', '.join(CATEGORIES)}")
    return value

def valid_payment_mode(value: str) -> str:
    value = {"Upi":"UPI","Bank transfer":"Bank Transfer"}.get(value.strip().title(), value.strip().title())
    if value not in PAYMENT_MODES: raise ValueError(f"Unknown payment mode. Choose: {', '.join(PAYMENT_MODES)}")
    return value

def valid_month(value: str) -> str:
    value = value.strip()
    try: datetime.strptime(value, "%Y-%m")
    except ValueError as exc: raise ValueError("Month must use YYYY-MM format.") from exc
    return value
