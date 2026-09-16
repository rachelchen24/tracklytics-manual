"""
Manual athlete performance prediction model.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime
import helpers as hp
import visualizer as vz


CURR_YEAR = 2026


def dist_from_PB(athlete_id: int, score_year: int, event: str) -> float:
    """
    Calculate the average distance between an athlete's season marks
    and their personal best prior to the score year.

    Args:
        athlete_id: Unique identifier of the athlete.
        score_year: The season/year to source competition marks from.
        Must not be 2024.
        event: Discipline/event name to filter by.

    Returns:
        Mean difference between season marks and personal best as a float.
        Negative values indicate the athlete performed below
        their PB on average.
    """
    # Read data file. Gets full results
    athlete_data = hp.read_data(athlete_id)
    athlete_data = athlete_data[athlete_data['discipline'] == event]
    pb = hp.get_PB(athlete_id, event)

    dist = athlete_data[athlete_data['year'] == score_year]['mark'] - pb
    avg_dist = dist.mean()
    return avg_dist


def std_result_score(athlete_id: int, year: int) -> float:
    """
    Calculate the standard deviation of an athlete's result scores
    over a given year.

    Args:
        athlete_id: Unique identifier of the athlete.
        year: The season/year to filter results for.

    Returns:
        Standard deviation of result scores as a float. Returns NaN if
        fewer than two results are found.
    """
    athlete_data = hp.read_data(athlete_id)
    athlete_data = athlete_data[athlete_data['year'] == year]
    rscores = athlete_data['resultScore']
    return rscores.std()


def std_place(athlete_id: int, year: int) -> float:
    """
    Calculate the standard deviation of an athlete's placement
    over a given year.

    Args:
        athlete_id: Unique identifier of the athlete.
        year: The season/year to filter results for.

    Returns:
        Standard deviation of placement as a float. Returns NaN if
        fewer than two results are found.
    """
    athlete_data = hp.read_data(athlete_id)
    athlete_data = athlete_data[athlete_data['year'] == year]
    places = athlete_data['place']
    return places.std()


def win_rate(athlete_id: int, year: int, event: str = None) -> float:
    """
    Calculate the win rate (first-place finish ratio) for an athlete
    in a given year.

    Args:
        athlete_id: Unique identifier of the athlete.
        year: The season/year to filter results for.
        event: Discipline/event name to filter by.
        If None, all events are included.

    Returns:
        Win rate as a float between 0.0 and 1.0.
        Returns 0.0 if no results are found.
    """
    athlete_data = hp.read_data(athlete_id)
    if event is not None:
        athlete_data = athlete_data[athlete_data['discipline'] == event]
    if len(athlete_data) == 0:
        return 0.0
    wins = athlete_data[athlete_data['place'] == 1]
    return len(wins) / len(athlete_data)


def podium_rate(athlete_id: int, year: int, event: str = None) -> float:
    """
    Calculate the podium rate (top-three finish ratio)
    for an athlete in a given year.

    Args:
        athlete_id: Unique identifier of the athlete.
        year: The season/year to filter results for.
        event: Discipline/event name to filter by.
        If None, all events are included.

    Returns:
        Podium rate as a float between 0.0 and 1.0.
        Returns 0.0 if no results are found.
    """
    athlete_data = hp.read_data(athlete_id)
    if event is not None:
        athlete_data = athlete_data[athlete_data['discipline'] == event]
    if len(athlete_data) == 0:
        return 0.0
    podiums = athlete_data[athlete_data['place'] <= 3]
    return len(podiums) / len(athlete_data)


def champ_win_rate(athlete_id: int, year: int, event: str = None) -> float:
    """
    Calculate the champion win rate
    (first-place finish ratio at major championships)
    for an athlete in a given year.

    Args:
        athlete_id: Unique identifier of the athlete.
        year: The season/year to filter results for.
        event: Discipline/event name to filter by.
        If None, all events are included.

    Returns:
        Win rate as a float between 0.0 and 1.0.
        Returns 0.0 if no results are found.
    """
    athlete_data = hp.read_data(athlete_id)
    if event is not None:
        athlete_data = athlete_data[athlete_data['discipline'] == event]
    champ_mask = athlete_data['competition'].str.contains(
        'Championships|Olympic Games', na=False)
    champ_data = athlete_data[champ_mask]
    if len(champ_data) == 0:
        return 0.0
    wins = champ_data[champ_data['place'] == 1]
    return len(wins) / len(champ_data)


def champ_podium_rate(athlete_id: int, year: int, event: str = None) -> float:
    """
    Calculate the champion podium rate
    (top-three finish ratio at major championships)
    for an athlete in a given year.

    Args:
        athlete_id: Unique identifier of the athlete.
        year: The season/year to filter results for.
        event: Discipline/event name to filter by.
        If None, all events are included.

    Returns:
        Podium rate as a float between 0.0 and 1.0.
        Returns 0.0 if no results are found.
    """
    athlete_data = hp.read_data(athlete_id)
    if event is not None:
        athlete_data = athlete_data[athlete_data['discipline'] == event]
    champ_mask = athlete_data['competition'].str.contains(
        'Championships|Olympic Games', na=False)
    champ_data = athlete_data[champ_mask]
    if len(champ_data) == 0:
        return 0
    podiums = champ_data[champ_data['place'] <= 3]
    return len(podiums) / len(champ_data)


def avg_place(athlete_id: int, score_year: int, event: str = None) -> float:
    """
    Calculate average placement for an athlete in a given year and event.

    Args:
        athlete_id: Unique identifier of the athlete.
        score_year: The season/year to filter results for.
        event: Discipline/event name to filter by.

    Returns:
        Mean placement as a float. Returns NaN if no results are found.
    """
    athlete_data = hp.read_data(athlete_id)
    athlete_data = athlete_data[(athlete_data['year'] == score_year)]
    if "Mile" in event:
        athlete_data = athlete_data[athlete_data['discipline'] == "Mile"]
    else:
        athlete_data = athlete_data[athlete_data['discipline'] == event]
    
    avg_place = athlete_data['place'].mean()
    return round(avg_place, 2)


def avg_result_score(athlete_id: int, score_year: int,
                     event: str = None) -> float:
    """
    Calculate average result score for an athlete in a given event.

    Args:
        athlete_id: Unique identifier of the athlete.
        score_year: The season/year to filter results for.
        event: Discipline/event name to filter by.

    Returns:
        Mean result score as a float. Returns NaN if no results are found.
    """
    #print(event)
    athlete_data = hp.read_data(athlete_id)
    athlete_data = athlete_data[(athlete_data['year'] == score_year)]
    #print(athlete_data)
    if "Mile" in event:
        athlete_data = athlete_data[athlete_data['discipline'] == "Mile"]
    else:
        athlete_data = athlete_data[athlete_data['discipline'] == event]
    avg_resultScore = athlete_data['resultScore'].mean()
    return round(avg_resultScore, 2)


def var_place(athlete_id: int, score_year: int, event: str = None) -> float:
    athlete_data = hp.read_data(athlete_id)
    var = athlete_data['place'].std()
    if var > 10:
        return 10
    elif var < 1:
        return 1
    # bounds var to be between 1 and 10, inclusive
    return round(var, 2)


def var_resultscore(athlete_id: int, score_year: int,
                    event: str = None) -> float:
    athlete_data = hp.read_data(athlete_id)
    var = athlete_data['resultScore'].mean()
    # want to bound to be between 1 and 10, inclusive
    # differ by 10 is a little, differ by 100+ is a lot
    return round(var, 2)


def get_consistency(athlete_id: int, score_year: int):
    place_var = var_place(athlete_id, score_year)
    rs_var = var_resultscore(athlete_id, score_year)
    consistency_score = 0.3 * (10 / place_var) + 0.7 * (100 / rs_var)
    return round(consistency_score, 2)


def predict_mark_linear(athlete_id: int, score_year: int, event: str) -> float:
    """
    Predict an athlete's performance mark at the 2026 World Championships
    using linear regression over their season marks.

    Args:
        athlete_id: Unique identifier of the athlete.
        score_year: The season/year to source competition marks from.
        event: Discipline/event name to filter by.

    Returns:
        Predicted performance mark at the championship date (2026-08-30).
    """
    champ_date = datetime(2026, 9, 11)
    athlete_data = hp.read_data(athlete_id)
    athlete_data = athlete_data[athlete_data['year'] == score_year]
    athlete_data = athlete_data[athlete_data['discipline'] == event]
    dates = pd.to_datetime(athlete_data['date'], format='%d %b %Y')
    date_nums = dates.map(pd.Timestamp.toordinal).values.reshape(-1, 1)

    marks = athlete_data['mark']
    lin_reg = LinearRegression()
    lin_reg.fit(date_nums, marks)

    prediction = lin_reg.predict([[champ_date.toordinal()]])
    return prediction[0]


def predict_mark_log(athlete_id: int, score_year: int, event: str) -> float:
    """
    Predict an athlete's performance mark at the 2026 World Championships
    using logarithmic progression model over their season marks.

    Args:
        athlete_id: Unique identifier of the athlete.
        score_year: The season/year to source competition marks from.
        event: Discipline/event name to filter by.

    Returns:
        Predicted performance mark at the championship date (2026-08-30).
    """
    champ_date = datetime(2026, 9, 11)
    print('searching for:', event)
    athlete_data = hp.read_data(athlete_id)
    athlete_data = athlete_data[athlete_data['year'] == score_year]
    if "Mile" in event:
        athlete_data = athlete_data[athlete_data['discipline'] == "Mile"]
    else:
        print('len before:', len(athlete_data))
        athlete_data = athlete_data[athlete_data['discipline'] == event]
        print('len after:', len(athlete_data))
    dates = pd.to_datetime(athlete_data['date'], format='%d %b %Y')
    marks = athlete_data['mark']
    print(len(marks))

    a = 0.12
    b = marks.iloc[0]

    def log_model(x):
        return a * np.log(x) + b

    future_x = champ_date.toordinal()
    future_x = future_x - dates.map(pd.Timestamp.toordinal).min() + 1

    prediction = log_model(future_x)
    prediction = round(prediction, 2)
    return hp.float_to_time(prediction)


def predict_resultscore_log(athlete_id: int, score_year: int, event: str) -> float:
    """
    Predict an athlete's result score at the 2026 World Championships
    using logarithmic progression model over their season result scores.

    Args:
        athlete_id: Unique identifier of the athlete.
        score_year: The season/year to source result scores from.

    Returns:
        Predicted result score at the championship date (2026-08-30).
    """
    champ_date = datetime(2026, 9, 11)
    athlete_data = hp.read_data(athlete_id)
    athlete_data = athlete_data[athlete_data['year'] == score_year]
    if "Mile" in event:
        athlete_data = athlete_data[athlete_data['discipline'] == "Mile"]
    else:
        athlete_data = athlete_data[athlete_data['discipline'] == event]
    dates = pd.to_datetime(athlete_data['date'], format='%d %b %Y')
    dates = pd.to_datetime(athlete_data['date'], format='%d %b %Y')

    rscores = athlete_data['resultScore']

    if len(rscores) == 0:
        return avg_result_score(athlete_id, score_year, event)

    a = 0.1
    b = rscores.iloc[0]

    def log_model(x):
        return a * np.log(x) + b

    future_x = champ_date.toordinal()
    future_x = future_x - dates.map(pd.Timestamp.toordinal).min() + 1

    prediction = log_model(future_x)
    return round(prediction, 2)


def predict_place_linear(athlete_id: int, score_year: int,
                         event: str) -> float:
    """
    Predict an athlete's placement at the 2026 World Championships
    using linear regression over their season placements.

    Args:
        athlete_id: Unique identifier of the athlete.
        score_year: The season/year to source placements from.
        event: Discipline/event name to filter by.

    Returns:
        Predicted placement at the championship date (2026-08-30).
    """
    champ_date = datetime(2026, 9, 11)
    athlete_data = hp.read_data(athlete_id)
    athlete_data = athlete_data[athlete_data['year'] == score_year]
    athlete_data = athlete_data[athlete_data['discipline'] == event]
    athlete_data = athlete_data.dropna(subset=['place'])

    dates = pd.to_datetime(athlete_data['date'], format='%d %b %Y')
    date_nums = dates.map(pd.Timestamp.toordinal).values.reshape(-1, 1)
    places = athlete_data['place']
    lin_reg = LinearRegression()
    lin_reg.fit(date_nums, places)
    future_x = [[champ_date.toordinal()]]
    prediction = lin_reg.predict(future_x)
    return prediction[0]


def predict_place_log(athlete_id: int, score_year: int, event: str) -> float:
    """
    Predict an athlete's placement at the 2026 World Championships
    using logarithmic progression model over their season placements.

    Args:
        athlete_id: Unique identifier of the athlete.
        score_year: The season/year to source placements from.
        event: Discipline/event name to filter by.

    Returns:
        Predicted placement at the championship date (2026-08-30).
    """
    champ_date = datetime(2026, 9, 11)
    athlete_data = hp.read_data(athlete_id)
    athlete_data = athlete_data[athlete_data['year'] == score_year]
    athlete_data = athlete_data[athlete_data['discipline'] == event]
    dates = pd.to_datetime(athlete_data['date'], format='%d %b %Y')

    places = athlete_data['place'].dropna()

    if len(places) == 0:
        return avg_place(athlete_id, score_year, event)

    a = 0.2
    b = places.iloc[0]

    def log_model(x):
        return a * np.log(x) + b
    future_x = champ_date.toordinal()
    future_x = future_x - dates.map(pd.Timestamp.toordinal).min() + 1

    prediction = log_model(future_x)
    return round(prediction, 2)


def current_stats(athlete_id: int) -> dict:
    athlete_data = hp.read_data(athlete_id)
    athlete_id = int(athlete_id)

    disciplines = hp.get_current_events(athlete_id)
    stats = {}
    stats["name"] = athlete_data["name"].iloc[0]
    stats["gender"] = athlete_data["gender"].iloc[0]
    stats["events"] = []
    stats["nerdstats"] = []

    cdob_filled = False

    for discp in disciplines:
        print(discp)
        event_df = pd.read_csv(
            f"event_files/{CURR_YEAR} {athlete_data['gender'].iloc[0]}s {discp}.csv"  # noqa: E501
        )

        if int(athlete_id) in event_df["athlete_id"].values:
            # if they are in the top list for that event
            # (cuz sometimes they're not)
            idx = event_df.index[event_df["athlete_id"] == int(athlete_id)][0]
            stats["events"].append({
                "event": discp,
                "pb": hp.float_to_time(hp.get_PB(athlete_id, discp)),
                "sb": hp.float_to_time(hp.get_SB(athlete_id, discp)),
                "world_rank": idx + 1,
            })
            stats["nerdstats"].append({
                "event": discp, 
                "avg_place": avg_place(athlete_id, CURR_YEAR, discp),
                "avg_result_score": avg_result_score(athlete_id, CURR_YEAR,
                                                     discp),
                "var_place": var_place(athlete_id, CURR_YEAR, discp),
                "var_resultscore": var_resultscore(athlete_id, CURR_YEAR,
                                                   discp),
                "pred_mark": predict_mark_log(athlete_id, CURR_YEAR, discp),
                "pred_place": predict_place_log(athlete_id, CURR_YEAR, discp),
                "predict_rs": predict_resultscore_log(athlete_id, CURR_YEAR, discp),
                "graph": vz.plot_reg(athlete_id, CURR_YEAR, discp)
            })

            if not cdob_filled:
                dob = event_df.loc[idx, "DOB"]
                stats["age"] = hp.get_age(dob)
                country = event_df.loc[idx, "Country"]
                stats["country"] = country
                cdob_filled = True

        else:
            # do almost the same thing except we keep world_rank null
            stats["events"].append({
                "event": discp,
                "pb": hp.float_to_time(hp.get_PB(athlete_id, discp)),
                "sb": hp.float_to_time(hp.get_SB(athlete_id, discp)),
                "world_rank": ">100",
            })
            stats["nerdstats"].append({
                "event": discp, 
                "avg_place": avg_place(athlete_id, CURR_YEAR, discp),
                "avg_result_score": avg_result_score(athlete_id, CURR_YEAR,
                                                     discp),
                "var_place": var_place(athlete_id, CURR_YEAR, discp),
                "var_resultscore": var_resultscore(athlete_id, CURR_YEAR,
                                                   discp),
                "pred_mark": predict_mark_log(athlete_id, CURR_YEAR, discp),
                "pred_place": predict_place_log(athlete_id, CURR_YEAR, discp),
                "predict_rs": predict_resultscore_log(athlete_id, CURR_YEAR,
                                                      discp),
                "graph": vz.plot_reg(athlete_id, CURR_YEAR, discp)
            })
            vz.plot_reg(athlete_id, CURR_YEAR, discp)

    # Placeholder values until I implement them
    # stats["results"] = []

    print(stats)
    return stats


def cumulative_score(athlete_id: int, score_year: int, event: str) -> float:
    """
    Compute a weighted overall score from an athlete's season
    performance metrics.

    Args:
        athlete_id: Unique identifier of the athlete.
        score_year: The season/year to source performance metrics from.
        event: Discipline/event name to filter by.

    Returns:
        Overall score as a float. Higher is better.
    """
    # between 0 and 1
    overall_w_rate = win_rate(athlete_id, score_year, event)

    # between 0 and 1
    overall_pod_rate = podium_rate(athlete_id, score_year, event)

    # between 0 and 1
    champ_w_rate = champ_win_rate(athlete_id, score_year, event)

    # between 0 and 1
    champ_pod_rate = champ_podium_rate(athlete_id, score_year, event)

    # between 1 and 20, typically
    mean_place = avg_place(athlete_id, score_year, event)

    # between 800 and 1300
    mean_resultscore = avg_result_score(athlete_id, score_year, event)

    # between 800 and 1300
    predicted_resultscore = predict_resultscore_log(athlete_id, score_year,
                                                    event)

    resultscore_std = std_result_score(athlete_id, score_year)

    # between 1 and 20
    predicted_place = predict_place_log(athlete_id, score_year, event)

    season_success = 0.5 * overall_w_rate + 0.5 * overall_pod_rate
    championship_success = 0.6 * champ_w_rate + 0.4 * champ_pod_rate
    clutch = championship_success - season_success

    norm_resultscore = (mean_resultscore - 800) / (1300 - 800)
    norm_pred_resultscore = (predicted_resultscore - 800) / 500

    norm_place = 1 / np.log(mean_place + 1)
    norm_pred_place = 1 / np.log(predicted_place + 1)
    consistency_rs = resultscore_std / mean_resultscore

    # between 0 and 1: if positive, they are a better racer in
    # championship races. If negative, then they have no championship "edge"
    score = (0.17 * season_success +
             0.12 * championship_success +
             0.20 * norm_resultscore +
             0.15 * norm_pred_resultscore +
             0.16 * norm_place +
             0.10 * norm_pred_place +
             0.05 * consistency_rs +
             0.05 * clutch)
    # print(athlete_id, 0.17 * season_success, 0.12 * championship_success,
    # 0.17 * norm_pred_resultscore, 0.11 * norm_pred_resultscore,
    # 0.17 * norm_place, 0.11 * norm_pred_place, 0.05 * consistency_rs,
    # 0.05 * consistency_place, 0.05 * clutch)
    # print()
    # 14695983
    return score


def main():
    mens5kdata = pd.read_csv("event_files/2026 Mens 5000 Metres.csv")

    mens5kdata = mens5kdata[:25]
    scores = {}
    for _, row in mens5kdata.iterrows():
        runner_id = row["athlete_id"]
        name = row["Competitor"]
        scores[name] = float(cumulative_score(runner_id, 2026, "5000 Metres"))
    sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1],
                                reverse=True))
    n = 1
    for person in sorted_scores:
        print(n, person, sorted_scores[person])
        n += 1


if __name__ == '__main__':
    main()
