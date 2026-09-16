"""
File containing all the helper methods used in both predictors
and the EDA
"""

import pandas as pd
import numpy as np
from datetime import datetime, date
import manual_predictor as mp


YEARS = [2022, 2023, 2024, 2025, 2026]

CURR_YEAR = 2026

OLYMPIC_EVENTS = [
    "100 Metres",
    "200 Metres",
    "400 Metres",
    "800 Metres",
    "1500 Metres",
    "Mile",
    "5000 Metres",
    "10,000 Metres",
    "100 Metres Hurdles",
    "400 Metres Hurdles",
    "3000 Metres Steeplechase",
    "High Jump",
    "Pole Vault",
    "Long Jump",
    "Triple Jump",
    "Shot Put",
    "Discus Throw",
    "Hammer Throw",
    "Javelin Throw",
    "Marathon",
]


def setup() -> pd.DataFrame:
    all_athletes = pd.read_csv('athlete_files/all_athletes.csv', header=None)
    all_athletes.loc[2] = (
        all_athletes.loc[1]
        .str.replace(r"[^A-Za-z0-9]", "", regex=True)
        .str.lower()
    )
    # all_athletes.to_csv("athlete_files/all_athletes.csv", index=False)
    return all_athletes


all_athletes = setup()


def add_year_df(athlete_id: int) -> pd.DataFrame:
    """
    Will add a 'year' column to given athlete's csv data. Helps
    easily access year for any meet an athlete did.
    """
    # Read csv
    athlete_data = pd.read_csv("athlete_files/" + str(athlete_id) + '.csv')

    # Make list consisting of the last 4 characters, e.g. the year
    # from the date
    dates = athlete_data['date']
    year = [int(date[-4:]) for date in dates]

    # Create new column
    athlete_data['year'] = year
    athlete_data['year'] = athlete_data['year'].astype(int)
    return athlete_data


def read_data(athlete_id: int, event: str = None,
              year: int = None) -> pd.DataFrame:
    """
    Does 5 basic tasks:
    1. Reads csv
    2. Gets rid of relay events - keeps only individual events
    3. Adds year to df
    4. Changes all places to float
    5. Changes all marks to float
    6. Assimilates indoor and outdoor races of the same distance to be
    the same event
    So all 6 are enveloped in one function
    and we only need to pass in the ID
    """
    athlete_data = pd.read_csv("athlete_files/" + str(athlete_id) + '.csv')
    individual_mask = athlete_data['discipline'].str.contains('Relay',
                                                              na=False)
    athlete_data = athlete_data[~individual_mask]
    athlete_data = add_year_df(athlete_id)
    athlete_data['place'] = pd.to_numeric(athlete_data['place'],
                                          errors='coerce')
    athlete_data = athlete_data.dropna(subset=['place'])
    athlete_data['place'] = athlete_data['place'].astype(int)
    athlete_data = athlete_data.dropna(subset=['mark'])
    athlete_data['mark'] = athlete_data['mark'].apply(to_float)
    athlete_data = assim_indoor_outdoor(athlete_data)
    return athlete_data


def read_for_html(athlete_id: int) -> pd.DataFrame:
    athlete_data = pd.read_csv("athlete_files/" + str(athlete_id) + '.csv')
    individual_mask = athlete_data['discipline'].str.contains('Relay',
                                                              na=False)
    athlete_data = athlete_data[~individual_mask]
    athlete_data = add_year_df(athlete_id)
    athlete_data['place'] = pd.to_numeric(athlete_data['place'],
                                          errors='coerce')
    athlete_data = athlete_data.dropna(subset=['place'])
    athlete_data['place'] = athlete_data['place'].astype(int)
    athlete_data = athlete_data.dropna(subset=['mark'])
    athlete_data = assim_indoor_outdoor(athlete_data)
    return athlete_data


def get_event(gender_event: str):
    words = gender_event.split(" ")
    words = words[1:]
    event = ''
    for word in words:
        event += ' ' + word
    return event


def running(event: str):
    """
    Checks if the event is a running event based on whether the event string
    contains the key words 'Metres', 'Marathon', or 'Mile'
    """
    return any(word in event for word in ['Metres', 'Marathon', 'Mile'])


def get_PB(athlete_id: int, event: str) -> float:
    """
    Gets overall PB
    """
    athlete_data = read_data(athlete_id)
    if event == "One Mile":
        event = "Mile"
    results = athlete_data[athlete_data['discipline'] == event]
    if running(event):
        return results['mark'].min()
    else:
        return results['mark'].max()


def get_SB(athlete_id: int, event: str) -> float:
    """
    Gets Season Best
    Null if no results yet
    """
    athlete_data = read_data(athlete_id)
    if event == "One Mile":
        event = "Mile"
    results = athlete_data[athlete_data['year'] == CURR_YEAR]
    results = results[results['discipline'] == event]
    if running(event):
        return results['mark'].min()
    else:
        return results['mark'].max()


def get_worldrank(athlete_id: int, event: str) -> float:
    """
    Parses event files to find given athlete's world rank
    Full event name should be given
    """
    event_data = pd.read_csv("event_files/" + str(CURR_YEAR)
                             + " " + event + ".csv")
    return event_data.loc[event_data['athlete_id']
                          == athlete_id, 'Rank'].iloc[0]


def parse_place(val) -> float:
    """
    Parse place values like '1.', '2', '1sf1' → float or NaN.
    """
    s = str(val).strip().rstrip('.')
    digits = ''
    for character in s:
        if character.isdigit():
            digits += character
        else:
            break
    if digits:
        return float(digits)
    return np.nan


def to_float(mark: str) -> float:
    """
    Converts str representation of mark into float for readability.
    Ignores DQs and DNs. If mark is in seconds, additional process
    is required to convert str representation of time to float.
    """
    mark = str(mark)  # cast to string so we can check if ':' is in it
    mark = mark.replace("h", "")  # that appears in some apparently
    if 'D' in mark or 'N' in mark:
        # we just skip over it
        pass
    elif ':' in mark:
        units = mark.split(":")
        if len(units) == 3:
            # then it is a marathon results in order hh:mm:ss
            return int(units[0]) * 3600 + int(units[1]) * 60 + int(units[2])
        else:
            # it is a mm:ss.ms results
            return int(units[0]) * 60 + float(units[1])

    else:
        return float(mark)


def assim_indoor_outdoor(athlete_dataframe: pd.DataFrame) -> pd.DataFrame:
    # If it contains "Short Track, just get rid of that"
    mask = athlete_dataframe['discipline'].str.contains('Short Track',
                                                        na=False)
    athlete_dataframe.loc[mask, 'discipline'] = (
        athlete_dataframe.loc[mask, 'discipline'].str[:-12]
    )

    return athlete_dataframe


def get_discipline(event_file: str) -> str:
    """
    Extract discipline from filename:
    e.g. "2024 Men's 100 Metres.csv" → "100 Metres".
    """
    event = " ".join(event_file.split()[-2:])
    event = event[:-4]
    return event



def get_rankings(event: str) -> pd.DataFrame:
    """
    Returns df containing the event file for the given event
    The given event should contain the gender we want to investigate
    e.g. Women's/Men's
    """
    ranking_df = pd.read_csv("event_files/" + str(CURR_YEAR) + " "
                             + event + ".csv")
    return ranking_df[['Rank', 'Mark', 'Competitor', 'DOB', 'Country',
                       'Venue', 'Date', 'Results Score']]


def get_events(athlete_id: int) -> set:
    ath_disciplines = set()
    athlete_data = read_data(athlete_id)
    for discp in athlete_data['discipline']:
        if discp in OLYMPIC_EVENTS:
            if discp == "Mile":
                ath_disciplines.add("One Mile")
            else:
                ath_disciplines.add(discp)
    return ath_disciplines


def get_current_events(athlete_id: int) -> set:
    ath_disciplines = set()
    athlete_data = read_data(athlete_id)
    current_data = athlete_data[athlete_data['date'].str[-4:] == str(CURR_YEAR)]
    for discp in current_data['discipline']:
        if discp in OLYMPIC_EVENTS:
            if discp == "Mile":
                ath_disciplines.add("One Mile")
            else:
                ath_disciplines.add(discp)
    return ath_disciplines


def get_events_year(athlete_id: int, year) -> set:
    ath_disciplines = set()
    athlete_data = read_data(athlete_id)
    current_data = athlete_data[athlete_data['date'].str[-4:] == str(year)]
    for discp in current_data['discipline']:
        if discp in OLYMPIC_EVENTS:
            if discp == "Mile":
                ath_disciplines.add("One Mile")
            else:
                ath_disciplines.add(discp)
    return ath_disciplines


def get_age(dob: str) -> int:
    if dob is None:
        return 0
    dob = datetime.strptime(dob, "%d %b %Y").date()
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) <
                                   (dob.month, dob.day))
    return age


def get_id_from_name(name_ns: str) -> int:
    """
    Looks through all_athletes dictionary to find the id corresponding with
    the athlete
    Assumes there are no two athletes with the same name
    name_ns means name no space
    """
    col = (all_athletes.iloc[1] == name_ns).idxmax()
    idnum = all_athletes.iloc[0, col]
    return idnum


def float_to_time(time: float) -> str:
    """
    Turns float to time
    """
    if time is None:
        return ""
    elif time >= 3600:
        # if over an hour, i.e. marathon in hh:mm:ss
        hours = int(time // 3600)
        time -= hours * 3600
        # minutes, seconds are left
        minutes = int(time // 60)
        seconds = int(time - minutes * 60)
        return str(hours) + ':' + add0(minutes) + ':' + add0(seconds)
    elif time >= 60:
        # not over an hour, but over a minute, in form mm:ss.ms
        minutes = int(time // 60)
        time -= minutes * 60
        # only seconds are left
        seconds = int(time)
        # truncate off the decimals
        milliseconds = int((time - seconds) * 100)
        return str(minutes) + ':' + add0(seconds) + '.' + add0(milliseconds)
    elif time < 60:
        seconds = int(time)
        milliseconds = int((time - seconds) * 100)
        return add0(seconds) + '.' + add0(milliseconds)
    else:
        return ""


def add0(num: int) -> str:
    if num < 10:
        return '0' + str(num)
    else:
        return str(num)
