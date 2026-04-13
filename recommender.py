import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load data and prepare the engine
df = pd.read_csv("data/drinks.csv")
feature_cols = ["sweet", "bitter", "alcoholic", "citric", "refreshing"]
features = df[feature_cols]
similarity_matrix = cosine_similarity(features)

def get_smart_recommendations(drink_selected):
    try:
        idx = df[df["drink"] == drink_selected].index[0]
    except:
        return {}

    scores = list(enumerate(similarity_matrix[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:]
    
    recs = {"Classic": None, "Signature": None, "Non-Alcoholic": None}
    
    for i, score in scores:
        row = df.iloc[i]
        cat = row["category"]
        if cat in recs and recs[cat] is None:
            recs[cat] = {
                "drink": row["drink"],
                "price": row["price"],
                "reason": row["pairing_reason"],
                "image": row.get("image", ""),
                "similarity": score,
                "food": row["food"]
            }
        if all(recs.values()): break
    return recs