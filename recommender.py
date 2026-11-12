from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "drinks.csv"
FEATURE_COLUMNS = ["sweet", "bitter", "alcoholic", "citric", "refreshing"]
TARGET_CATEGORIES = ["Classic", "Signature", "Non-Alcoholic"]
REQUIRED_COLUMNS = {
    "drink",
    "category",
    "price",
    "ingredients",
    "food",
    "pairing_reason",
    "image",
    *FEATURE_COLUMNS,
}


def validate_drinks(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a clean copy of the drink dataset or raise a useful error."""
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    if frame.empty:
        raise ValueError("Drink dataset is empty")

    result = frame.copy()
    if result[list(REQUIRED_COLUMNS)].isna().any().any():
        raise ValueError("Required fields cannot be empty")
    for column in ["drink", "category", "ingredients", "food", "pairing_reason"]:
        result[column] = result[column].astype(str).str.strip()
        if result[column].eq("").any():
            raise ValueError(f"{column} cannot be blank")

    if result["drink"].str.casefold().duplicated().any():
        raise ValueError("Drink names must be unique")

    result[FEATURE_COLUMNS] = result[FEATURE_COLUMNS].apply(
        pd.to_numeric, errors="raise"
    )
    scores_are_valid = result[FEATURE_COLUMNS].apply(
        lambda values: values.between(0, 5)
    )
    if not scores_are_valid.all().all():
        raise ValueError("Flavor scores must be between 0 and 5")
    if result[FEATURE_COLUMNS].sum(axis=1).eq(0).any():
        raise ValueError("Every drink needs at least one positive flavor score")

    result["price"] = pd.to_numeric(result["price"], errors="raise")
    if not result["price"].map(lambda price: 0 < price < float("inf")).all():
        raise ValueError("Prices must be finite and greater than zero")

    missing_categories = set(TARGET_CATEGORIES).difference(result["category"])
    if missing_categories:
        raise ValueError(
            f"Missing recommendation categories: {sorted(missing_categories)}"
        )

    return result


def load_drinks(path: Path = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Load and validate a CSV drink dataset."""
    return validate_drinks(pd.read_csv(path))


def get_smart_recommendations(
    drink_selected: str,
    drinks: pd.DataFrame | None = None,
) -> dict[str, dict[str, object]]:
    """Return the closest drink in each target category using cosine similarity."""
    frame = load_drinks() if drinks is None else validate_drinks(drinks)
    matches = frame.index[frame["drink"] == drink_selected].tolist()
    if not matches:
        raise ValueError(f"Unknown drink: {drink_selected}")

    selected_index = matches[0]
    similarity_matrix = cosine_similarity(frame[FEATURE_COLUMNS])
    scores = [
        (index, float(score))
        for index, score in enumerate(similarity_matrix[selected_index])
        if index != selected_index
    ]
    scores.sort(key=lambda item: item[1], reverse=True)

    recommendations: dict[str, dict[str, object]] = {}
    for index, score in scores:
        row = frame.iloc[index]
        category = row["category"]
        if category in TARGET_CATEGORIES and category not in recommendations:
            recommendations[category] = {
                "drink": row["drink"],
                "price": float(row["price"]),
                "reason": row["pairing_reason"],
                "image": row["image"],
                "similarity": score,
                "food": row["food"],
            }
        if len(recommendations) == len(TARGET_CATEGORIES):
            break

    return recommendations
