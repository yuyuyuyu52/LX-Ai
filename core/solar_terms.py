from datetime import date

# Approximate coefficients for 24 solar terms (节气)
# Each entry: (month, constant)
SOLAR_TERMS = {
    "小寒": (1, 5.4055),
    "大寒": (1, 20.12),
    "立春": (2, 3.87),
    "雨水": (2, 18.73),
    "惊蛰": (3, 5.63),
    "春分": (3, 20.646),
    "清明": (4, 4.81),
    "谷雨": (4, 20.1),
    "立夏": (5, 5.52),
    "小满": (5, 21.04),
    "芒种": (6, 5.678),
    "夏至": (6, 21.37),
    "小暑": (7, 7.108),
    "大暑": (7, 22.83),
    "立秋": (8, 7.5),
    "处暑": (8, 23.13),
    "白露": (9, 7.646),
    "秋分": (9, 23.042),
    "寒露": (10, 8.318),
    "霜降": (10, 23.438),
    "立冬": (11, 7.438),
    "小雪": (11, 22.36),
    "大雪": (12, 7.18),
    "冬至": (12, 21.94),
}

# Known year corrections for certain terms (year, term) -> delta days
TERM_CORRECTIONS = {
    (2026, "小寒"): 1,
}

def solar_term_date(year: int, term: str) -> date:
    """Return approximate Gregorian date for the solar term."""
    if term not in SOLAR_TERMS:
        raise ValueError(f"Unknown solar term: {term}")
    month, C = SOLAR_TERMS[term]
    if year >= 2000:
        y = year - 2000
        day = int(y * 0.2422 + C) - int((y - 1) / 4)
    else:
        y = year - 1900
        day = int(y * 0.2422 + C) - int(y / 4)
    day += TERM_CORRECTIONS.get((year, term), 0)
    return date(year, month, day)
