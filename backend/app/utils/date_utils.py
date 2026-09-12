from datetime import date, timedelta


def trip_dates(start: date, days: int) -> list[date]:
    return [start + timedelta(days=index) for index in range(days)]
