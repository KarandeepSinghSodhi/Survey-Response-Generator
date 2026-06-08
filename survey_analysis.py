import io
from typing import Dict, Tuple
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    analysis_df = df[["satisfaction", "nps"]].copy()
    analysis_df["delivery_numeric"] = df["delivery"].map({"Yes": 1, "No": 0})
    return analysis_df.corr()


def conditional_probabilities(df: pd.DataFrame) -> Dict[str, float]:
    total_high = df[df["satisfaction"] >= 4].shape[0]
    total_low = df[df["satisfaction"] <= 2].shape[0]
    total_delivery_yes = df[df["delivery"] == "Yes"].shape[0]
    total_delivery_no = df[df["delivery"] == "No"].shape[0]

    return {
        "p_nps_high_given_satisfaction_high":
            df[(df["satisfaction"] >= 4) & (df["nps"] >= 8)].shape[0] / max(1, total_high),
        "p_nps_high_given_satisfaction_low":
            df[(df["satisfaction"] <= 2) & (df["nps"] >= 8)].shape[0] / max(1, total_low),
        "p_satisfaction_high_given_delivery_yes":
            df[(df["delivery"] == "Yes") & (df["satisfaction"] >= 4)].shape[0] / max(1, total_delivery_yes),
        "p_satisfaction_high_given_delivery_no":
            df[(df["delivery"] == "No") & (df["satisfaction"] >= 4)].shape[0] / max(1, total_delivery_no),
    }


def distribution_metrics(df: pd.DataFrame) -> Dict[str, Dict]:
    return {
        "satisfaction": df["satisfaction"].value_counts().sort_index().to_dict(),
        "nps": df["nps"].value_counts().sort_index().to_dict(),
        "category": df["category"].value_counts().sort_index().to_dict(),
        "delivery": df["delivery"].value_counts().sort_index().to_dict(),
    }


def text_diversity_metrics(df: pd.DataFrame) -> Dict[str, float]:
    total = len(df)
    unique = df["feedback"].nunique()
    duplicates = total - unique
    duplicate_rate = duplicates / total
    lengths = df["feedback"].str.split().str.len()
    return {
        "unique_feedback": unique,
        "duplicate_rate": duplicate_rate,
        "unique_percentage": unique / total,
        "average_feedback_length": float(lengths.mean()),
        "median_feedback_length": float(lengths.median()),
    }


def persona_recovery(df: pd.DataFrame) -> Dict[str, object]:
    df = df.copy()
    df["persona"] = df["satisfaction"].apply(
        lambda x: "Happy" if x >= 4 else "Neutral" if x == 3 else "Unhappy"
    )
    feature_df = pd.get_dummies(df[["category", "delivery"]], drop_first=True)
    feature_df["nps"] = df["nps"]
    feature_df["satisfaction"] = df["satisfaction"]
    feature_df["text_length"] = df["feedback"].str.split().str.len()

    X = feature_df.values
    y = df["persona"].values
    label_counts = df["persona"].value_counts()
    stratify = y if label_counts.min() >= 2 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        stratify=stratify,
        test_size=0.2,
        random_state=42,
    )

    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    report = classification_report(y_test, y_pred, output_dict=True)
    cm = confusion_matrix(y_test, y_pred, labels=["Happy", "Neutral", "Unhappy"])

    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "classification_report": report,
        "confusion_matrix": cm.tolist(),
        "labels": ["Happy", "Neutral", "Unhappy"],
    }
