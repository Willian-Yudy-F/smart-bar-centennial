# 🍸 Smart Bar — Centennial Staff Intelligence


## In plain English
I was a bartender for years, and I know that under pressure staff recommend the drinks they remember — usually the cheap classics. This app gives them a better answer in one tap: pick what the guest ordered and it suggests the closest **signature cocktail** (plus a classic and a non-alcoholic option) and explains *why* the flavours match. Under the hood each drink is a vector of five flavour scores and **scikit-learn** finds the nearest neighbours with cosine similarity.

**What I learned:** turning domain knowledge from a real job into a dataset, and building a tiny recommender system with pandas, scikit-learn and Streamlit.

An AI-powered drink-pairing assistant that helps bar staff turn classic drink orders into signature cocktail sales.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![scikit--learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikitlearn&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=white)

## The Problem

Bar staff know the menu, but under pressure they default to the drinks they remember — usually the classics. Signature cocktails ($24–$32) sit on the menu with no systematic way to recommend them.

## The Solution

This app gives staff an instant, flavor-based recommendation for any drink a guest orders or shows interest in:

1. Each drink is profiled across five flavor dimensions: **sweet, bitter, alcoholic, citric, refreshing**
2. A **cosine-similarity matrix** (scikit-learn) finds the closest matches across the menu
3. For every selection, the app returns the best pairing in each category — **Classic**, **Signature** and **Non-Alcoholic** — with the pairing reason and a food match

Staff see *why* the recommendation works, so they can explain it to the guest naturally.

## How It Works

```
data/drinks.csv ──► flavor feature matrix ──► cosine similarity ──► top match per category
                    (sweet, bitter, ...)      (scikit-learn)        (Classic / Signature / N-A)
```

## Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project Structure

| File | Purpose |
|------|---------|
| `app.py` | Streamlit UI — drink selection, pairing cards, strategy context |
| `recommender.py` | Similarity engine — builds the flavor matrix and returns recommendations |
| `data/drinks.csv` | Drink database: category, price, ingredients, flavor profile, food pairing |
| `data/scraper.py` | Data collection helper |

## Tech Stack

- **Python** — core language
- **Streamlit** — interactive web UI
- **pandas** — data handling
- **scikit-learn** — cosine similarity for flavor matching

---

*Built by [Willian Yudy Futema](https://github.com/Willian-Yudy-F) — IT student in Sydney focused on data analytics.*
