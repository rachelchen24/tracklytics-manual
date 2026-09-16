# Import statements
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
import helpers as hp


# Palette for all our following visualizations
my_palette = ['#FFC107', '#FF3830', '#00BFA5', '#3D8BFF', '#B388FF', '#F2F4F7']


def summary7n(athlete_id: int, event: str, year: int) -> list[int]:
    """
    Reads in athlete data and returns 7 number summary of athlete marks
    and results score.
    Seven number summary includes: mean, standard deviation, minimum,
    first quartile,
    median, third quartile, and maximum.
    """
    # Read csv
    athlete_data = hp.read_data(athlete_id, year, event)

    # Filter
    athlete_data = athlete_data[(athlete_data['discipline']
                                 == event) & (athlete_data['year'] == year)]

    # Create a Series from mark column, converted to type float
    marks = athlete_data['mark'].apply(hp.to_float)

    # 7 num summary for mark:
    marks_summary = get_summary(marks)

    # Create a Series from resultScore column
    # 7 num sum for resultScore:
    result_scores = athlete_data['resultScore']
    rs_summary = get_summary(result_scores)
    return (marks_summary, rs_summary)


def get_summary(data: pd.Series) -> list[float]:
    """
    Returns seven number summary of a list or Pandas Series. Helper method
    for formal 7-number-summary methods.
    """
    summary = [data.mean(), data.std(), data.min(), data.quantile(0.25),
               data.median(), data.quantile(0.75), data.max()]
    return [round(float(val), 2) for val in summary]


def print_7n_summary_individual(details: list[str], marks_summary: list[float],
                                scores_summary: list[float]) -> None:
    """
    Prints athlete marks and results score from seven number summary
    in a readable fashion.
    """
    print(details[0], details[1], details[2] + ' Results: ')
    print("[mean, standard deviation, minimum, first quartile, median, third quartile, maximum]")  # noqa: E501
    print("Marks:", marks_summary)
    print("Scores", scores_summary)


def event_7n_summary(event_name: str) -> tuple[list[float], list[float]]:
    """
    Reads in event data and returns 7 number summary of event marks and
    results score.
    Seven number summary includes: mean, standard deviation, minimum,
    first quartile, median, third quartile, and maximum.
    """
    # Read csv
    event_data = pd.read_csv('event_files/' + event_name + '.csv')

    # Create a Series from mark column, converted to type float
    marks = event_data['Mark'].apply(hp.to_float)

    # Create a Series from mark column
    # 7 num summary for mark:
    marks_summary = get_summary(marks)

    # Create a Series from resultScore column
    # 7 num sum for resultScore:
    result_scores = event_data['Results Score']
    rs_summary = get_summary(result_scores)
    return (marks_summary, rs_summary)


def print_7n_summary_event(event: str, marks_summary: list[float],
                           scores_summary: list[float]) -> None:
    """
    Prints event marks and results score from seven number summary
    in a readable fashion.
    """
    print(event, "Results:")
    print("[mean, standard deviation, minimum, first quartile, median, third quartile, maximum]")  # noqa: E501
    print("Marks:", marks_summary)
    print("Scores", scores_summary)


def event_boxplot(event: str) -> None:
    """
    Plots boxplot visualization of given event, given the full name of
    an existing csv.
    """
    event_df = pd.read_csv("event_files/" + event + ".csv")

    # Plot
    fig, [ax1, ax2] = plt.subplots(1, 2, figsize=(15, 7))

    sns.boxplot(data=event_df, y='Mark', ax=ax1, color=my_palette[1])
    ax1.set_title(event + " Yearly Mark Distribution", fontsize=18)
    ax1.set_ylabel("Mark (m)", fontsize=16)
    ax1.yaxis.set_major_locator(MaxNLocator(nbins=6))  # ~6 ticks max

    if hp.running(event):
        # then it is a running event
        # and we reverse x axis since lower time is good result score
        ax1.invert_yaxis()
        ax1.set_ylabel("Mark (s)", fontsize=16)

    sns.boxplot(data=event_df, y='Results Score', ax=ax2, color=my_palette[2])
    ax2.set_title(event + " Yearly Result Score Distribution", fontsize=18)
    ax2.set_ylabel("Results Score", fontsize=16)
    plt.tight_layout()
    plt.savefig('plots/' + event + ' boxplot.png')


def athlete_boxplot(athlete_id: int, event: str) -> None:
    """
    Plots boxplot visualization of given athlete, given the event that
    we would like to plot and the athlete's ID number
    """
    athlete_df = pd.read_csv("athlete_files/" + str(athlete_id) + ".csv")
    name = athlete_df['name'][0]
    athlete_df = athlete_df[athlete_df['discipline'] == event]

    # Plot
    fig, [ax1, ax2] = plt.subplots(1, 2, figsize=(15, 7))

    sns.boxplot(data=athlete_df, y='mark', ax=ax1, color=my_palette[1])
    ax1.set_title(name + " Yearly Mark Distribution", fontsize=18)
    ax1.set_ylabel("Mark (m)", fontsize=16)
    # limits amount of ticks on y axis
    ax1.yaxis.set_major_locator(MaxNLocator(nbins=6))

    if hp.running(event):
        # then it is a running event
        # and we reverse x axis since lower time is good result score
        # ax1.invert_yaxis()
        ax1.set_ylabel("Mark (in time)", fontsize=16)

    sns.boxplot(data=athlete_df, y='resultScore', ax=ax2, color=my_palette[2])
    ax2.set_title(name + " Yearly Result Score Distribution", fontsize=18)
    ax2.set_ylabel("Results Score", fontsize=16)
    plt.tight_layout()
    plt.savefig('plots/' + str(athlete_id) + ' boxplot.png')


def plot_reg(athlete_id, year, event):
    """
    Uses a DataFrame-based approach to plot athlete trajectory
    using linear regression. Requires year and event specification
    to pinpoint which data to analyze.
    """
    # Filter date
    athlete_data = hp.read_data(athlete_id)
    athlete_data = athlete_data[athlete_data['year'] == year]
    athlete_data['date'] = pd.to_datetime(athlete_data['date'],
                                          format='%d %b %Y')

    # Filter events
    if "Mile" in event:
        athlete_data = athlete_data[athlete_data['discipline'] == "Mile"]
    else:
        athlete_data = athlete_data[athlete_data['discipline'] == event]
    athlete_data['mark'] = [hp.to_float(mark) for mark in athlete_data['mark']]

    # Change date to num
    athlete_data['date_num'] = mdates.date2num(athlete_data['date'])
    plt.figure(figsize=(10, 6))
    sns.regplot(data=athlete_data, x='date_num', y='mark')
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b %Y'))

    ax.set_title(event + " Season Trajectory")
    ax.set_xlabel("Date")
    ax.set_ylabel("Mark (s)")
    plt.xticks(rotation=45)
    title = 'plots/' + str(athlete_id) + ' ' + event + ' regplot.png'
    plt.savefig('static/' + title)
    plt.close()

    return title


def plot_mark_v_score(event: str) -> None:
    """
    Plots given event's mark and results score distribution with histogram.
    """
    df = pd.read_csv("event_files/" + event + ".csv")
    df['Mark'] = df['Mark'].apply(hp.to_float)
    fig, [ax1, ax2] = plt.subplots(1, 2, figsize=(15, 7))

    # Set background color
    ax1.set_facecolor(my_palette[2])
    ax2.set_facecolor(my_palette[2])

    sns.histplot(data=df, x='Mark', bins=8, ax=ax1, color=my_palette[1],
                 edgecolor='white', linewidth=1.5)
    ax1.set_title(event + " Mark Distribution", fontsize=15)
    ax1.set_xlabel("Mark (m)", fontsize=16)
    ax1.set_ylabel("Frequency", fontsize=16)
    if hp.running(event):
        # then it is a running event
        # and we reverse x axis since lower time is good result score
        ax1.set_xlim(df['Mark'].min(), df['Mark'].max())
        ax1.invert_xaxis()
        ax1.set_xlabel("Mark (s)", fontsize=16)

    sns.histplot(data=df, x='Results Score', bins=8, ax=ax2,
                 color=my_palette[1], edgecolor='white', linewidth=1.5)
    ax2.set_title(event + " Results Score Distribution", fontsize=15)
    ax2.set_xlabel("Results Score", fontsize=16)
    ax2.set_ylabel("Frequency", fontsize=16)
    ax2.set_xlim(df['Results Score'].min(), df['Results Score'].max())

    plt.tight_layout()
    plt.savefig('plots/' + event + ' mark_v_score.png')


def trackflation_visualizer(specific_event: str) -> float:
    """
    Plots a boxplot depicting yearly mark and result score distribution
    of the top 100 athletes in the given specific event. Returns the
    trackflation index (mean mark in 2026 / mean mark in 2024)
    """
    years = [2024, 2025, 2026]
    events = [pd.read_csv(
        "event_files/" + str(year) + ' ' + specific_event + '.csv'
        ) for year in years]

    for year, event in zip(years, events):
        event['year'] = year
        event['Mark'] = event['Mark'].apply(hp.to_float)

    combined = pd.concat(events, ignore_index=True)

    mark_means = combined.groupby('year')['Mark'].mean()
    score_means = combined.groupby('year')['Results Score'].mean()

    # Plot
    fig, [ax1, ax2] = plt.subplots(1, 2, figsize=(15, 7))

    sns.boxplot(data=combined, x='year', y='Mark', ax=ax1, color=my_palette[1])
    ax1.plot([0, 1, 2], [mark_means[y] for y in years], color=my_palette[0],
             marker='o', linewidth=2, label='Mean')
    ax1.legend()
    ax1.set_title(specific_event + " Yearly Mark Distribution", fontsize=18)
    ax1.set_xlabel("Year", fontsize=16)
    ax1.set_ylabel("Mark (m)", fontsize=16)
    # ax1.set_facecolor('#9494F6')

    # reverse y axis (for running) since lower time is good result score
    if hp.running(specific_event):
        ax1.invert_yaxis()
        ax1.set_ylabel("Mark (s)", fontsize=16)

    sns.boxplot(data=combined, x='year', y='Results Score', ax=ax2,
                color=my_palette[2])
    ax2.plot([0, 1, 2], [score_means[y] for y in years], color=my_palette[0],
             marker='o', linewidth=2, label='Mean')
    ax2.legend()
    ax2.set_title(specific_event + " Yearly Result Score Distribution",
                  fontsize=18)
    ax2.set_xlabel("Year", fontsize=16)
    ax2.set_ylabel("Results Score", fontsize=16)
    plt.tight_layout()
    plt.savefig('plots/' + specific_event + ' trackflation.png')

    trackflation_index = round(mark_means[2026] / mark_means[2024], 4)
    return trackflation_index


def athlete_growth(athlete_id: int, event: str) -> None:
    """
    Plots a violin plot of an athletes yearly mark performance in the
    given event.
    """
    # Read csv
    athlete_data = pd.read_csv("athlete_files/" + str(athlete_id) + '.csv')

    # First, add year to df
    athlete_data = hp.add_year_df(athlete_id)

    # Get name
    name = athlete_data['name'][0]

    # Change 'date' column to be datetime objects
    athlete_data['date'] = pd.to_datetime(athlete_data['date'],
                                          format='%d %b %Y')
    # Get just 5k performances
    athlete_data = athlete_data[athlete_data['discipline'] == event]

    athlete_data['mark'] = athlete_data['mark'].apply(hp.to_float)
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot
    sns.violinplot(data=athlete_data, x='year', y='mark', palette=my_palette,
                   ax=ax, hue='year', legend=False, inner="box",
                   inner_kws={"box_width": 15, "linewidth": 4})
    ax.set_title(name + " Yearly Mark Distribution", fontsize=18)
    ax.set_xlabel("Year", fontsize=16)
    ax.set_ylabel("Mark (m)", fontsize=16)

    # reverse y axis (for running) since lower time is good result score
    if hp.running(event):
        # it is a running event, we invert the axis so that a lower
        # time is "better"
        ax.invert_yaxis()
        ax.set_ylabel("Mark (s)", fontsize=16)

    plt.tight_layout()
    plt.savefig('plots/' + str(athlete_id) + ' ' + event + ' growth.png')


def main():
    # Prints the 7-number-summary for Grant Fisher's performances
    # across the 5000 Metres in the 2025 season.
    athlete_id = 14591210
    name = pd.read_csv('athlete_files/' + str(athlete_id) + '.csv')['name'][0]
    event = "5000 Metres"
    year = 2025

    details = [name, year, event]
    marks_summary, scores_summary = summary7n(athlete_id, event, year)
    print_7n_summary_individual(details, marks_summary, scores_summary)

    # Prints the 7-number-summary for Danil Lysenko's performances across the
    # High Jump in the 2025 season.
    athlete_id = 14576019
    name = pd.read_csv('athlete_files/' + str(athlete_id) + '.csv')['name'][0]
    event = "High Jump"
    year = 2025

    details = [name, year, event]
    marks_summary, scores_summary = summary7n(athlete_id, event, year)
    print_7n_summary_individual(details, marks_summary, scores_summary)

    # Prints the 7-number-summary for the top 100 results in the
    # Women's 100 Metres Hurdles across the 2026 season.
    event_name = "2026 Women's 100 Metres Hurdles"
    marks_summary, scores_summary = event_7n_summary(event_name)
    print_7n_summary_event(event_name, marks_summary, scores_summary)

    # Shows the distribution of performances and results scores across the
    # 2024 Men's Marathon.
    event_boxplot("2024 Men's Marathon")

    # Shows the distribution of performances and results scores across
    # the 2024 Women's Discus Throw.
    event_boxplot("2024 Women's Discus Throw")

    # Shows Jane Hedengren's distribution of performances and results scores
    # across the 5000 Metres for all three years, 2024, 2025, and 2026.
    athlete_boxplot(15090151, '5000 Metres')

    # Shows Blessed Owusu Jr.'s distribution of performances and results scores
    # across the 400 Metres for all three years, 2024, 2025, and 2026.
    athlete_boxplot(15302671, '400 Metres')

    # Shows Grant Fisher's progression over the 2025 season with a linear
    # regression plot
    plot_reg(14591210, 2025, '5000 Metres')

    # Plots boxplots for mark and result score for the 2026 Women's Triple Jump
    plot_mark_v_score("2026 Women's Triple Jump")

    # Plots boxplots for mark and result score for the 2025 Women's 1500 Metres
    plot_mark_v_score("2025 Women's 1500 Metres")

    # Plots and calculates the trackflation index for the Women's Triple Jump
    print(trackflation_visualizer("Women's Triple Jump"))

    # Plots and calculates the trackflation index for the Men's Shot Put
    print(trackflation_visualizer("Men's Shot Put"))

    # Plots and calculates the trackflation index for the Men's 400 Metres
    print(trackflation_visualizer("Men's 400 Metres"))

    # Plots violin plot for Grant Fisher in the 5000 Metres.
    athlete_growth(14591210, "5000 Metres")


if __name__ == '__main__':
    main()
