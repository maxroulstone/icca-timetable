import numpy as np
import pandas as pd
from datetime import datetime
import os

from icalendar import Calendar, Event
import pytz

def get_personal_timetable(groups: list[str]) -> pd.DataFrame:
    """
    This function creates a personal timetable for a student based on the groups they are in.

    Args:
    groups: dict[str] - a dictionary with the student's groups

    Returns:
    pd.DataFrame - a timetable for the next 7 days
    """
    # Type safety of groups
    if not isinstance(groups, list):
        raise TypeError("groups must be a list")
    
    if not all(isinstance(group, str) for group in groups):
        raise TypeError("all elements in groups must be strings")
    
    # Get full timetable
    main_df = pd.read_csv('data/timetable.csv')

    filtered_df = main_df[main_df['group'].isin(groups)].sort_values(by=['date', 'time'])

    print('Success:', filtered_df.head())

    return filtered_df

def csv_to_ics(csv_input, output_file="timetable.ics"):
    """
    Convert a CSV timetable to an ICS (iCalendar) file.
    
    Parameters:
    - csv_input: Path to CSV file (str) or pandas DataFrame
    - output_file: Path to save the ICS file (default: "timetable.ics")
    """
    # Load CSV into DataFrame if a file path is provided
    if isinstance(csv_input, str):
        df = pd.read_csv(csv_input)
    elif isinstance(csv_input, pd.DataFrame):
        df = csv_input
    else:
        raise ValueError("csv_input must be a file path (str) or pandas DataFrame")

    # Initialize the calendar
    cal = Calendar()
    cal.add('prodid', 'Max Roulstone')
    cal.add('version', '2.0')

    # Set timezone (assuming UTC; adjust if needed)
    timezone = pytz.UTC

    # Process each row in the DataFrame
    for _, row in df.iterrows():
        # Parse date and time
        event_date = datetime.strptime(row['date'], '%Y-%m-%d')
        start_time, end_time = row['time'].split('-')
        start_dt = timezone.localize(datetime.strptime(f"{row['date']} {start_time}", '%Y-%m-%d %H:%M'))
        end_dt = timezone.localize(datetime.strptime(f"{row['date']} {end_time}", '%Y-%m-%d %H:%M'))

        # Create an event
        event = Event()
        event.add('dtstart', start_dt)
        event.add('dtend', end_dt)
        event.add('summary', f"{row['class']} Session {row['session']}")
        event.add('location', row['room'])
        event.add('description', f"Group: {row['room']}, Tutor: {row['tutor']}")
        event.add('uid', f"{start_dt.strftime('%Y%m%dT%H%M%S')}-{row['room']}@mr")  # Unique ID

        # Add event to calendar
        cal.add_component(event)

    # Write to ICS file
    with open(output_file, 'wb') as f:
        f.write(cal.to_ical())
    print(f"ICS file saved as {output_file}")

    return cal.to_ical()

if __name__ == "__main__":
    # Example usage
    groups = ['9', '9ii']
    print(get_personal_timetable(groups))

    