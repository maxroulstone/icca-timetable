import numpy as np
import pandas as pd
import datetime
import os

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

    return filtered_df

if __name__ == "__main__":
    # Example usage
    groups = ['9', '9ii']
    print(get_personal_timetable(groups))

    