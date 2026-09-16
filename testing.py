"""
Checks for missing values in athlete and event data files.
"""

import pandas as pd

ATHLETE_DIR = "athlete_files"
EVENT_DIR = "event_files"


def check_missing_values(file_names: list) -> None:
    for file in file_names:
        df = pd.read_csv(file)
        for column in df.columns:
            missing_rows = df.loc[df[column].isna()]
            if len(missing_rows) > 0:
                print("\nFile: " + str(file))
                print("Column: " + str(column))
                missing_list = [i + 2 for i in missing_rows.index.tolist()]
                print(
                    "Lines with missing values: " + str(missing_list)
                    )


if __name__ == "__main__":
    athlete_files = ["athlete_files/14164861.csv",
                     "athlete_files/14165762.csv",
                     "athlete_files/14166878.csv"]

    event_files = ["event_files/2024 Men's 5000 Metres.csv",
                   "event_files/2025 Men's 100 Metres.csv",
                   "event_files/2026 Women's 110 Metres Hurdles.csv"]

    check_missing_values(athlete_files)
    check_missing_values(event_files)
