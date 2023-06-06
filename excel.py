import os
import pandas as pd
from datetime import datetime

# create excel file to store multipliers
def create_excel_file(filename):
    if not os.path.exists(filename):
        df = pd.DataFrame(columns=['rodada','datetime', 'multiplier'])
        df.to_excel(filename, index=False)
        print(f"{filename} created successfully!")


def add_row_to_excel(filename: str, rodada:int, datetime: datetime, multiplier:float):
    create_excel_file(filename)

    df = pd.DataFrame({'rodada': [rodada],'datetime': [datetime], 'multiplier': [multiplier]})
    with pd.ExcelWriter(filename, mode='a',  if_sheet_exists="overlay") as writer:
        start_row = writer.sheets['Sheet1'].max_row
        df.to_excel(writer, index=False, header=False, startrow=start_row)
        print(f"multiplier added to {filename}: {rodada = } {datetime = } {multiplier = }")