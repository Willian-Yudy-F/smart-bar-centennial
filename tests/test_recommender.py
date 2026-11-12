from __future__ import annotations

import pandas as pd
import pytest

from recommender import (
    FEATURE_COLUMNS,
    TARGET_CATEGORIES,
    get_smart_recommendations,
    load_drinks,
    validate_drinks,
)


def test_default_dataset_is_valid() -> None:
    drinks = load_drinks()
    assert len(drinks) == 14
    assert set(TARGET_CATEGORIES).issubset(set(drinks["category"]))


def test_recommendations_cover_each_target_category() -> None:
    recommendations = get_smart_recommendations("Seasonal Martini")
    assert set(recommendations) == set(TARGET_CATEGORIES)
    assert all(item["drink"] != "Seasonal Martini" for item in recommendations.values())
    assert all(0 <= item["similarity"] <= 1 for item in recommendations.values())


def test_unknown_drink_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown drink"):
        get_smart_recommendations("Missing Drink")


def test_missing_column_is_rejected() -> None:
    frame = load_drinks().drop(columns=["food"])
    with pytest.raises(ValueError, match="Missing columns"):
        validate_drinks(frame)


def test_duplicate_drink_names_are_rejected() -> None:
    frame = load_drinks()
    duplicate = frame.iloc[[0]].copy()
    duplicate["drink"] = duplicate["drink"].str.upper()
    frame = pd.concat([frame, duplicate], ignore_index=True)
    with pytest.raises(ValueError, match="unique"):
        validate_drinks(frame)


def test_out_of_range_flavour_score_is_rejected() -> None:
    frame = load_drinks()
    frame.loc[0, FEATURE_COLUMNS[0]] = 6
    with pytest.raises(ValueError, match="between 0 and 5"):
        validate_drinks(frame)


def test_missing_required_value_is_rejected() -> None:
    frame = load_drinks()
    frame.loc[0, "food"] = None
    with pytest.raises(ValueError, match="cannot be empty"):
        validate_drinks(frame)
