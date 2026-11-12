from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from recommender import get_smart_recommendations, load_drinks


PROJECT_ROOT = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Smart Bar Pairing Assistant",
    page_icon="🍸",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data() -> pd.DataFrame:
    return load_drinks()


def show_drink_image(image_value: object) -> None:
    image = str(image_value).strip()
    if image.startswith(("https://", "http://")):
        st.image(image, use_container_width=True)
        return

    local_path = PROJECT_ROOT / image
    if image and local_path.is_file():
        st.image(local_path, use_container_width=True)
    else:
        st.info("Image unavailable for this drink.")


drinks = load_data()

st.title("🍸 Smart Bar Pairing Assistant")
st.subheader("A transparent, flavour-based recommendation prototype")

with st.expander("How this prototype works"):
    st.write(
        "Each drink has five manually assigned flavour scores. Cosine similarity "
        "compares those scores and returns the closest available Classic, Signature "
        "and Non-Alcoholic option. It does not use customer data or predict sales."
    )

selected_drink = st.selectbox(
    "Guest interest or current drink:",
    drinks["drink"].tolist(),
)
selected = drinks.loc[drinks["drink"] == selected_drink].iloc[0]

image_column, info_column = st.columns([1, 1.5])

with image_column:
    show_drink_image(selected["image"])

with info_column:
    st.header(selected_drink)
    st.write(f"**Ingredients:** {selected['ingredients']}")
    st.write(f"**Demo price:** ${selected['price']:.0f}")
    with st.container(border=True):
        st.subheader("🍴 Food pairing")
        st.write(f"**Suggested dish:** {selected['food']}")
        st.write(selected["pairing_reason"])

st.divider()

if st.button("Generate pairings", type="primary"):
    recommendations = get_smart_recommendations(selected_drink, drinks)
    st.markdown("### Similar options by category")
    columns = st.columns(3)
    titles = {
        "Classic": "🏛️ Similar Classic",
        "Signature": "✨ Signature Alternative",
        "Non-Alcoholic": "🥤 Non-Alcoholic Option",
    }

    for column, (category, title) in zip(columns, titles.items()):
        with column:
            recommendation = recommendations.get(category)
            if recommendation is None:
                st.warning(f"No {category} option is available.")
                continue

            st.markdown(f"#### {title}")
            show_drink_image(recommendation["image"])
            st.metric(recommendation["drink"], f"${recommendation['price']:.0f}")
            with st.expander("Pairing explanation"):
                st.write(f"**Why:** {recommendation['reason']}")
                st.write(f"**Food pairing:** {recommendation['food']}")
            st.progress(
                recommendation["similarity"],
                text=f"Flavour match: {recommendation['similarity']:.0%}",
            )
