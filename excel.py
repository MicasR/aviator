import os
import pandas as pd
from datetime import datetime


def create_columns_list(number_of_payouts:int=60)->list[str]:
    column_list = ['event_number','datetime', 'multiplier']
    for number in range(number_of_payouts): column_list.append(f"payout_{number}")
    return column_list


def create_excel_file(filename):
    if not os.path.exists(filename):
        df = pd.DataFrame(columns = create_columns_list())
        df.to_excel(filename, index=False)
        print(f"{filename} created successfully!")


def add_row_to_excel(filename: str, event_number:int, datetime: datetime, multiplier:float, payout_history: list[float]):
    create_excel_file(filename)

    df = pd.DataFrame({
        'event_number': [event_number],
        'datetime': [datetime],
        'multiplier': [multiplier],
        **{f'payout_{i}': [payout] for i, payout in enumerate(payout_history)}
    })

    with pd.ExcelWriter(filename, mode='a',  if_sheet_exists="overlay") as writer:
        start_row = writer.sheets['Sheet1'].max_row
        df.to_excel(writer, index=False, header=False, startrow=start_row)
        print(f"multiplier added to {filename}: {event_number = } {datetime = } {multiplier = } {len(payout_history) = }")