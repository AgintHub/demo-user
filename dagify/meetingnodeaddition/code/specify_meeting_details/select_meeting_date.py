from pydantic import BaseModel, Field
from typing import List
import re
import datetime
from dateutil import parser

class DateRange(BaseModel):
    start_date: str = Field(...)
    end_date: str = Field(...)

def select_meeting_date(dates: str) -> str:
    """
    This function selects a meeting date from a list of proposed dates based on certain criteria or user input.

    Args:
    dates: Input parameter of type str, expected to be a comma-separated list of dates.

    Returns:
    str: Output of type str, representing the selected meeting date.
    """
    # Assuming dates is a comma-separated string of date strings
    date_list = [date.strip() for date in dates.split(',')]

    # Simple implementation: Select the earliest valid date
    valid_dates = []
    for date_str in date_list:
        try:
            # Attempt to parse the date string into a datetime object
            date_obj = parser.parse(date_str)
            valid_dates.append(date_obj)
        except ValueError:
            # Handle dates that cannot be parsed
            print(f"Invalid date format: {date_str}")

    if not valid_dates:
        raise ValueError("No valid dates provided")

    # Select the earliest date
    selected_date = min(valid_dates)
    return selected_date.strftime('%Y-%m-%d')
