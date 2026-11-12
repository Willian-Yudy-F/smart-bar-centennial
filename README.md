# Smart Bar Pairing Assistant

[![CI](https://github.com/Willian-Yudy-F/smart-bar-centennial/actions/workflows/ci.yml/badge.svg)](https://github.com/Willian-Yudy-F/smart-bar-centennial/actions/workflows/ci.yml)

A small content-based recommender that helps bar staff compare drinks by flavour profile.
Select one drink and the Streamlit app returns the closest Classic, Signature and
Non-Alcoholic option available, together with a short pairing explanation. A category is
omitted when the selected drink is its only example in the demonstration dataset.

## Why I built it

After seven years in hospitality, I knew that menu knowledge becomes harder to apply
during a busy service. This prototype explores how a simple, explainable tool could help
staff recall alternatives without hiding the reasoning behind a black-box score.

This is a portfolio demonstration, not a production sales system. It does not use guest
profiles, transaction history or a trained predictive model.

## How it works

Each drink is represented by five manually assigned scores from 0 to 5:

- sweet;
- bitter;
- alcoholic;
- citric;
- refreshing.

The recommender calculates cosine similarity between those vectors, removes the selected
drink and returns the highest-scoring available option in each target category.

```text
data/drinks.csv
      │
      ▼
validate required fields and score ranges
      │
      ▼
build five-feature matrix
      │
      ▼
calculate cosine similarity
      │
      ▼
return one available result per target category
```

## What the score means

A high match means two drinks point in a similar direction across the five chosen flavour
dimensions. It does not mean a guest will buy or enjoy the recommendation. The attributes
are manually scored hypotheses, and the demo prices are not live venue data.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Run the automated checks with:

```bash
pytest -q
```

## Project structure

```text
app.py                 Streamlit interface
recommender.py         validation and similarity engine
data/drinks.csv        demonstration menu and flavour scores
data/images/           local supporting images
tests/                 recommender and dataset tests
```

## Design decisions

- Use a transparent content-based method instead of calling the prototype “AI-powered”.
- Validate the CSV before calculating recommendations.
- Resolve project files from the repository directory so the app does not depend on the
  terminal's current folder.
- Keep the engine separate from Streamlit so it can be tested without opening the UI.
- Remove the unfinished web scraper; menu updates should use a documented, permitted data
  source rather than placeholder scraping code.

## Limitations

- Only 14 demonstration drinks are included.
- Flavour scores are manually assigned and have not been validated with guests or staff.
- Cosine similarity ignores price preference, allergies, availability and service context.
- Image URLs depend on third-party hosting unless a local image is provided.
- No sales uplift or return on investment has been measured.

## Possible next step

The separate Bar Demand Analytics idea should use synthetic or properly anonymised event
sales data to forecast staffing and stock. It should not be presented as evidence that
this pairing prototype improves revenue.

---

Willian Yudy Futema · [Portfolio](https://willian-yudy-f.github.io/) ·
[LinkedIn](https://www.linkedin.com/in/willian-yudy-futema/)
