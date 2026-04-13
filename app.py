import streamlit as st
import pandas as pd
from recommender import get_smart_recommendations
import os

st.set_page_config(page_title="Centennial Staff Intelligence", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .pairing-card { background-color: #1c2128; border-left: 5px solid #58a6ff; padding: 20px; border-radius: 8px; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("data/drinks.csv")

df = load_data()

st.title("🍸 Centennial Staff Intelligence")
st.subheader("Professional Training & Sales Assistant")

# Strategy Context
with st.expander("📊 Strategic Goal & ROI"):
    st.write("Convert Classic orders into Signature Cocktails ($24-$32) using flavor-matching AI.")

# Selection
selected_drink = st.selectbox("Guest interest or current drink:", df["drink"].tolist())
d = df[df["drink"] == selected_drink].iloc[0]

# UI Layout
col_img, col_info = st.columns([1, 1.5]) 

with col_img:
    img_path = d.get('image', "https://via.placeholder.com/500") 
    
    if str(img_path).startswith('data/'):
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        else:
            st.warning(f"Local file missing: {img_path}")
            st.image("https://via.placeholder.com/500?text=Photo+Required", use_container_width=True)
    else:
        st.image(img_path, use_container_width=True)

with col_info:
    st.header(selected_drink)
    st.write(f"**Ingredients:** {d['ingredients']}")
    st.write(f"**Price:** ${d['price']}")
    st.markdown(f"""
    <div class="pairing-card">
        <h4>🍴 Strategic Food Pairing</h4>
        <p><b>Recommended Dish:</b> {d['food']}</p>
        <p><i>{d['pairing_reason']}</i></p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

if st.button("🔍 Generate AI Upsell Strategy"):
    recs = get_smart_recommendations(selected_drink)
    st.markdown("### Recommendation Strategy:")
    cols = st.columns(3)
    
    titles = {"Classic": "🏛️ Similar Classic", "Signature": "✨ Signature Upsell", "Non-Alcoholic": "🥤 Zero Proof"}
    
    for i, (key, title) in enumerate(titles.items()):
        with cols[i]:
            r = recs.get(key)
            if r:
                st.markdown(f"#### {title}")
                st.image(r.get('image', ""), use_container_width=True)
                st.metric(r['drink'], f"${r['price']}")
                with st.expander("Sales Argument"):
                    st.write(f"**Why:** {r['reason']}")
                    st.write(f"**Add-on:** {r['food']}")
                    st.progress(r['similarity'], text=f"Flavor Match: {int(r['similarity']*100)}%")