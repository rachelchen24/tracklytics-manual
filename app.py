from flask import Flask, render_template, request, jsonify
import pandas as pd
import helpers as hp
import manual_predictor as mp
import tree_predictor as tp
import visualizer as vs


app = Flask(__name__)
EVENTS = {
    "men/100": "Mens 100 Metres",
    "men/200": "Mens 200 Metres",
    "men/400": "Mens 400 Metres",
    "men/800": "Mens 800 Metres",
    "men/1500": "Mens 1500 Metres",
    "men/mile": "Mens One Mile",
    "men/5000": "Mens 5000 Metres",
    "men/10k": "Mens 10,000 Metres",
    "men/marathon": "Mens Marathon",
    "men/110h": "Mens 110 Metres Hurdles",
    "men/400h": "Mens 400 Metres Hurdles",
    "men/3ksteeple": "Mens 3000 Metres Steeplechase",
    "men/disc": "Mens Discus Throw",
    "men/hammer": "Mens Hammer Throw",
    "men/highjump": "Mens High Jump",
    "men/javelin": "Mens Javelin Throw",
    "men/longjump": "Mens Long Jump",
    "men/polevault": "Mens Pole Vault",
    "men/shot": "Mens Shot Put",
    "men/triplejump": "Mens Triple Jump",
    "women/100": "Womens 100 Metres",
    "women/200": "Womens 200 Metres",
    "women/400": "Womens 400 Metres",
    "women/800": "Womens 800 Metres",
    "women/1500": "Womens 1500 Metres",
    "women/mile": "Womens One Mile",
    "women/5000": "Womens 5000 Metres",
    "women/10k": "Womens 10,000 Metres",
    "women/marathon": "Womens Marathon",
    "women/100h": "Womens 100 Metres Hurdles",
    "women/400h": "Womens 400 Metres Hurdles",
    "women/3ksteeple": "Womens 3000 Metres Steeplechase",
    "women/disc": "Womens Discus Throw",
    "women/hammer": "Womens Hammer Throw",
    "women/highjump": "Womens High Jump",
    "women/javelin": "Womens Javelin Throw",
    "women/longjump": "Womens Long Jump",
    "women/polevault": "Womens Pole Vault",
    "women/shot": "Womens Shot Put",
    "women/triplejump": "Womens Triple Jump",
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
