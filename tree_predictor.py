"""
Random Forest classifier to predict athlete rankings at a championship meet.
"""

import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from datetime import datetime
import manual_predictor as mp
import helpers
from sklearn.ensemble import RandomForestClassifier


ATHLETE_DIR = "athlete_files"

TRAIN_YEAR = 2025
PREDICT_YEAR = 2026

CHAMP_DATE = datetime(2026, 9, 11)

FIELD_KEYWORDS = ["jump", "throw", "vault", "put"]

FILES_2024 = [
    "event_files/2024 Mens 100 Metres.csv",
    "event_files/2024 Mens 200 Metres.csv",
    "event_files/2024 Mens 400 Metres.csv",
    "event_files/2024 Mens 800 Metres.csv",
    "event_files/2024 Mens 1500 Metres.csv",
    "event_files/2024 Mens One Mile.csv",
    "event_files/2024 Mens 5000 Metres.csv",
    "event_files/2024 Mens 10,000 Metres.csv",
    "event_files/2024 Mens 110 Metres Hurdles.csv",
    "event_files/2024 Mens 400 Metres Hurdles.csv",
    "event_files/2024 Mens 3000 Metres Steeplechase.csv",
    "event_files/2024 Mens High Jump.csv",
    "event_files/2024 Mens Pole Vault.csv",
    "event_files/2024 Mens Long Jump.csv",
    "event_files/2024 Mens Triple Jump.csv",
    "event_files/2024 Mens Shot Put.csv",
    "event_files/2024 Mens Discus Throw.csv",
    "event_files/2024 Mens Hammer Throw.csv",
    "event_files/2024 Mens Javelin Throw.csv",
    "event_files/2024 Mens Marathon.csv",
    "event_files/2024 Womens 100 Metres.csv",
    "event_files/2024 Womens 200 Metres.csv",
    "event_files/2024 Womens 400 Metres.csv",
    "event_files/2024 Womens 800 Metres.csv",
    "event_files/2024 Womens 1500 Metres.csv",
    "event_files/2024 Womens One Mile.csv",
    "event_files/2024 Womens 5000 Metres.csv",
    "event_files/2024 Womens 10,000 Metres.csv",
    "event_files/2024 Womens 100 Metres Hurdles.csv",
    "event_files/2024 Womens 400 Metres Hurdles.csv",
    "event_files/2024 Womens 3000 Metres Steeplechase.csv",
    "event_files/2024 Womens High Jump.csv",
    "event_files/2024 Womens Pole Vault.csv",
    "event_files/2024 Womens Long Jump.csv",
    "event_files/2024 Womens Triple Jump.csv",
    "event_files/2024 Womens Shot Put.csv",
    "event_files/2024 Womens Discus Throw.csv",
    "event_files/2024 Womens Hammer Throw.csv",
    "event_files/2024 Womens Javelin Throw.csv",
    "event_files/2024 Womens Marathon.csv",
]

FILES_2025 = [
    "event_files/2025 Mens 100 Metres.csv",
    "event_files/2025 Mens 200 Metres.csv",
    "event_files/2025 Mens 400 Metres.csv",
    "event_files/2025 Mens 800 Metres.csv",
    "event_files/2025 Mens 1500 Metres.csv",
    "event_files/2025 Mens One Mile.csv",
    "event_files/2025 Mens 5000 Metres.csv",
    "event_files/2025 Mens 10,000 Metres.csv",
    "event_files/2025 Mens 110 Metres Hurdles.csv",
    "event_files/2025 Mens 400 Metres Hurdles.csv",
    "event_files/2025 Mens 3000 Metres Steeplechase.csv",
    "event_files/2025 Mens High Jump.csv",
    "event_files/2025 Mens Pole Vault.csv",
    "event_files/2025 Mens Long Jump.csv",
    "event_files/2025 Mens Triple Jump.csv",
    "event_files/2025 Mens Shot Put.csv",
    "event_files/2025 Mens Discus Throw.csv",
    "event_files/2025 Mens Hammer Throw.csv",
    "event_files/2025 Mens Javelin Throw.csv",
    "event_files/2025 Mens Marathon.csv",
    "event_files/2025 Womens 100 Metres.csv",
    "event_files/2025 Womens 200 Metres.csv",
    "event_files/2025 Womens 400 Metres.csv",
    "event_files/2025 Womens 800 Metres.csv",
    "event_files/2025 Womens 1500 Metres.csv",
    "event_files/2025 Womens One Mile.csv",
    "event_files/2025 Womens 5000 Metres.csv",
    "event_files/2025 Womens 10,000 Metres.csv",
    "event_files/2025 Womens 100 Metres Hurdles.csv",
    "event_files/2025 Womens 400 Metres Hurdles.csv",
    "event_files/2025 Womens 3000 Metres Steeplechase.csv",
    "event_files/2025 Womens High Jump.csv",
    "event_files/2025 Womens Pole Vault.csv",
    "event_files/2025 Womens Long Jump.csv",
    "event_files/2025 Womens Triple Jump.csv",
    "event_files/2025 Womens Shot Put.csv",
    "event_files/2025 Womens Discus Throw.csv",
    "event_files/2025 Womens Hammer Throw.csv",
    "event_files/2025 Womens Javelin Throw.csv",
    "event_files/2025 Womens Marathon.csv",
]

FILES_2026 = [
    "event_files/2026 Mens 100 Metres.csv",
    "event_files/2026 Mens 200 Metres.csv",
    "event_files/2026 Mens 400 Metres.csv",
    "event_files/2026 Mens 800 Metres.csv",
    "event_files/2026 Mens 1500 Metres.csv",
    "event_files/2026 Mens One Mile.csv",
    "event_files/2026 Mens 5000 Metres.csv",
    "event_files/2026 Mens 10,000 Metres.csv",
    "event_files/2026 Mens 110 Metres Hurdles.csv",
    "event_files/2026 Mens 400 Metres Hurdles.csv",
    "event_files/2026 Mens 3000 Metres Steeplechase.csv",
    "event_files/2026 Mens High Jump.csv",
    "event_files/2026 Mens Pole Vault.csv",
    "event_files/2026 Mens Long Jump.csv",
    "event_files/2026 Mens Triple Jump.csv",
    "event_files/2026 Mens Shot Put.csv",
    "event_files/2026 Mens Discus Throw.csv",
    "event_files/2026 Mens Hammer Throw.csv",
    "event_files/2026 Mens Javelin Throw.csv",
    "event_files/2026 Mens Marathon.csv",
    "event_files/2026 Womens 100 Metres.csv",
    "event_files/2026 Womens 200 Metres.csv",
    "event_files/2026 Womens 400 Metres.csv",
    "event_files/2026 Womens 800 Metres.csv",
    "event_files/2026 Womens 1500 Metres.csv",
    "event_files/2026 Womens One Mile.csv",
    "event_files/2026 Womens 5000 Metres.csv",
    "event_files/2026 Womens 10,000 Metres.csv",
    "event_files/2026 Womens 100 Metres Hurdles.csv",
    "event_files/2026 Womens 400 Metres Hurdles.csv",
    "event_files/2026 Womens 3000 Metres Steeplechase.csv",
    "event_files/2026 Womens High Jump.csv",
    "event_files/2026 Womens Pole Vault.csv",
    "event_files/2026 Womens Long Jump.csv",
    "event_files/2026 Womens Triple Jump.csv",
    "event_files/2026 Womens Shot Put.csv",
    "event_files/2026 Womens Discus Throw.csv",
    "event_files/2026 Womens Hammer Throw.csv",
    "event_files/2026 Womens Javelin Throw.csv",
    "event_files/2026 Womens Marathon.csv",
]


def athlete_features(athlete_id: int, discipline: str,
                     score_year: int) -> dict | None:
    """
    Compute all performance features for a single athlete
    in a given year and discipline.

    Args:
        athlete_id: Unique identifier of the athlete.
        discipline: Discipline/event name to filter by.
        score_year: The season/year to source performance metrics from.

    Returns:
        Dictionary of computed feature values, or None if no data is found.464
    """
    
    #14533464
    df = helpers.read_data(athlete_id, discipline, score_year)
    if df.empty:
        return None
    return {
        "pb":               helpers.get_PB(athlete_id, discipline),
        "dist_from_pb":     mp.dist_from_PB(athlete_id, score_year,
                                            discipline),
        "win_rate":         mp.win_rate(athlete_id, score_year, discipline),
        "podium_rate":      mp.podium_rate(athlete_id, score_year, discipline),
        "avg_place":        mp.avg_place(athlete_id, score_year, discipline),
        "avg_result_score": mp.avg_result_score(athlete_id, score_year,
                                                discipline),
        "pred_time":        mp.predict_mark_log(athlete_id, score_year,
                                                discipline),
        "pred_place":       mp.predict_place_log(athlete_id, score_year,
                                                 discipline),
        "pred_rs":          mp.predict_resultscore_log(athlete_id, score_year,
                                                       discipline),
        "consistency_rs":   mp.std_result_score(athlete_id, score_year)
    }


def build_dataset(event_file: str, score_year: int) -> pd.DataFrame:
    """
    Build a feature and label dataset for all athletes in a given event file.

    Args:
        event_file: Path to the CSV file containing athlete results
        for an event.
        score_year: The season/year to source performance metrics from.

    Returns:
        DataFrame of athlete features and labels for given event.
    """
    df = pd.read_csv(event_file)
    df = df[:50]
    print(event_file)
    discipline = helpers.get_discipline(event_file)
    print(discipline)

    rows = []
    for _, row in df.iterrows():
        athlete_id = str(row.get("athlete_id", "")).strip()
        if not athlete_id:
            continue

        feats = athlete_features(athlete_id, discipline, score_year)
        if feats is None:
            continue

        rows.append({
            **feats,
            "world_score": pd.to_numeric(row.get("Results Score", np.nan),
                                         errors="coerce"),
            "event_rank":  pd.to_numeric(row.get("Rank", np.nan),
                                         errors="coerce"),
            "competitor":  row.get("Competitor", "Unknown"),
            "athlete_id":  athlete_id,
            "discipline":  discipline,
            "label":       1 if str(row.get("Pos", "")).strip() == "1" else 0,
        })
    return pd.DataFrame(rows)


FEATURE_COLS = [
    "pb",
    "dist_from_pb",
    "win_rate",
    "podium_rate",
    "avg_place",
    "avg_result_score",
    "pred_time",
    "pred_place",
    "pred_rs",
    "consistency_rs",
    "event_rank",
]


def prepare_training_data(event_filter: str = None) -> None:
    """
    Build and save training dataset from 2024 event files.

    Args:
        event_filter: Optional substring to filter event files by name.
                      If None, all training files are included.

    Returns:
        None. Saves results to training_data.csv.
    """
    if event_filter:
        files = []
        for f in FILES_2025:
            if event_filter in f:
                files.append(f)
    else:
        files = FILES_2025

    print(f"Preparing training data from {len(files)} event files...")
    parts = []
    for f in files:
        parts.append(build_dataset(f, TRAIN_YEAR))
    df = pd.concat(parts, ignore_index=True)
    # df = df.dropna(subset=["pb"])
    df.to_csv("training_data.csv", index=False)
    print(f"Saved training_data.csv ({len(df)} rows)\n")


def prepare_predict_data(event_filter: str = None) -> None:
    """
    Build and save prediction dataset from 2025 event files.

    Args:
        event_filter: Optional substring to filter event files by name.
                      If None, all prediction files are included.

    Returns:
        None. Saves results to predict_data.csv.
    """
    if event_filter:
        files = []
        for f in FILES_2026:
            if event_filter in f:
                files.append(f)
    else:
        files = FILES_2026
    print(f"Preparing predict data from {len(files)} event files...")
    parts = []
    for f in files:
        parts.append(build_dataset(f, PREDICT_YEAR))
    df = pd.concat(parts, ignore_index=True)
    df.to_csv("predict_data.csv", index=False)
    print(f"Saved predict_data.csv ({len(df)} rows)\n")


def train() -> tuple[RandomForestClassifier, pd.Series]:
    """
    Train a Random Forest classifier to predict first-place finishes.

    Reads training_data.csv, fills missing values with column medians,
    80/20 train-test split.

    Returns:
        A tuple of trained model and feature medians used for filling.
    """
    # Read in data
    data = pd.read_csv("training_data.csv")

    # Separate into features and labels
    features = data[FEATURE_COLS]
    labels = data["label"]
    features['pred_time'] = features['pred_time'].apply(helpers.to_float)

    print(features)
    medians = features.median(numeric_only=True)
    features = features.fillna(medians)

    feature_train, feature_test, label_train, label_test = train_test_split(
        features, labels, test_size=0.2, random_state=42, stratify=labels
    )

    # Create and train model
    model = RandomForestClassifier(
        n_estimators=500,
        max_depth=8,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=42
    )
    model.fit(feature_train, label_train)

    # Accuracy
    train_predictions = model.predict(feature_train)
    print("Train Accuracy:", accuracy_score(label_train, train_predictions))

    test_predictions = model.predict(feature_test)
    print("Test  Accuracy:", accuracy_score(label_test, test_predictions))
    print("=== Model Evaluation (held-out 20%) ===")
    print(classification_report(label_test, test_predictions,
                                target_names=["Not 1st", "1st Place"]))

    return model, medians


def predict(model: RandomForestClassifier, medians: pd.Series) -> None:
    """
    Print predicted rankings for each event.

    Args:
        model: Trained Random Forest classifier.
        medians: Feature medians used to fill missing values.

    Returns:
        None. Prints ranked predictions.
    """
    # Read in data
    data = pd.read_csv("predict_data.csv")

    # Make predictions
    features = data[FEATURE_COLS].fillna(medians)
    win_idx = list(model.classes_).index(1)
    features['pred_time'] = features['pred_time'].apply(helpers.to_float)
    data["win_probability"] = model.predict_proba(features)[:, win_idx]

    # Print rankings per event
    for discipline, group in data.groupby("discipline"):
        results = (
            group[["competitor", "win_probability", "pb", "avg_result_score",
                   "win_rate", "world_score"]]
            .sort_values("win_probability", ascending=False)
            .reset_index(drop=True)
        )
        results.index += 1

        for name, imp in zip(FEATURE_COLS, model.feature_importances_):
            print(name, imp)

        print(f"=== Predicted Rankings: {discipline} ===\n")
        print(results.head(20).to_string())
        top = results.iloc[0]
        print(f"\n>>> Predicted 1st Place: {top['competitor']} "
              f"(win probability: {top['win_probability']:.2%}) <<<\n")
        print("-" * 60)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    event_filter = "Mens 5000 Metres"

    prepare_training_data(event_filter)
    prepare_predict_data(event_filter)

    model, medians = train()
    predict(model, medians)


if __name__ == "__main__":
    main()
