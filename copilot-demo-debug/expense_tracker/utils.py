from typing import Optional

def parse_amount(text: str) -> float:
    """
    Accepts amounts like: 10, 10.50, $10.50
    """
    cleaned = text.replace("$", "").strip()

    # BUG: commas like "1,000" will crash
    value = float(cleaned)

    # BUG: "round" here can hide precision issues in tests; also inconsistent formatting later
    return round(value, 2)

def safe_int(text: str) -> Optional[int]:
    try:
        return int(text)
    except Exception:
        return None
