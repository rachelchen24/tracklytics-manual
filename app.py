from flask import Flask, render_template, request, jsonify
import pandas as pd
import helpers as hp
import manual_predictor as mp
import tree_predictor as tp
import visualizer as vs


app = Flask(__name__)
EVENTS = {
    "men/100": "Men's 100 Metres",
    "men/200": "Men's 200 Metres",
    "men/400": "Men's 400 Metres",
    "men/800": "Men's 800 Metres",
    "men/1500": "Men's 1500 Metres",
    "men/mile": "Men's One Mile",
    "men/5000": "Men's 5000 Metres",
    "men/10k": "Men's 10,000 Metres",
    "men/marathon": "Men's Marathon",
    "men/110h": "Men's 110 Metres Hurdles",
    "men/400h": "Men's 400 Metres Hurdles",
    "men/3ksteeple": "Men's 3000 Metres Steeplechase",
    "men/disc": "Men's Discus Throw",
    "men/hammer": "Men's Hammer Throw",
    "men/highjump": "Men's High Jump",
    "men/javelin": "Men's Javelin Throw",
    "men/longjump": "Men's Long Jump",
    "men/polevault": "Men's Pole Vault",
    "men/shot": "Men's Shot Put",
    "men/triplejump": "Men's Triple Jump",
    "women/100": "Women's 100 Metres",
    "women/200": "Women's 200 Metres",
    "women/400": "Women's 400 Metres",
    "women/800": "Women's 800 Metres",
    "women/1500": "Women's 1500 Metres",
    "women/mile": "Women's One Mile",
    "women/5000": "Women's 5000 Metres",
    "women/10k": "Women's 10,000 Metres",
    "women/marathon": "Women's Marathon",
    "women/100h": "Women's 100 Metres Hurdles",
    "women/400h": "Women's 400 Metres Hurdles",
    "women/3ksteeple": "Women's 3000 Metres Steeplechase",
    "women/disc": "Women's Discus Throw",
    "women/hammer": "Women's Hammer Throw",
    "women/highjump": "Women's High Jump",
    "women/javelin": "Women's Javelin Throw",
    "women/longjump": "Women's Long Jump",
    "women/polevault": "Women's Pole Vault",
    "women/shot": "Women's Shot Put",
    "women/triplejump": "Women's Triple Jump",
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/rankings/<path:event>")
def rankings(event):
    if event not in EVENTS:
        return "Event not found", 404

    df = hp.get_rankings(EVENTS[event])
    df["Competitor"] = df["Competitor"].apply(
        lambda x: f'<a href="/athlete/{x}">{x}</a>'
    )
    return df.to_html(index=False, escape=False)


@app.route("/athlete/<name_ns>")
def athlete(name_ns):
    print(name_ns)
    ath_id = hp.get_id_from_name(name_ns)
    print(ath_id)
    current_stats = mp.current_stats(ath_id)
    df = hp.read_for_html(ath_id)
    df = df.iloc[::-1]
    marks = df[['date', 'venue', 'discipline', 'mark', 'place']]
    return render_template("athlete.html", **current_stats, marks=marks)


@app.route("/search_athletes")
def search_athletes():
    query = request.args.get("q", "").lower()

    matches = hp.all_athletes.T
    matches.columns = ["id", "slug", "name"]

    matches = matches[
        matches["name"].str.contains(query, case=False, na=False)
    ].head(8)

    return matches[["slug", "name"]].to_dict("records")


@app.route("/api/athlete/<slug>")
def athlete_api(slug):

    athlete_id = hp.get_id_from_name(slug)

    return mp.current_stats(athlete_id)


app.run(debug=True)
