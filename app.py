# streamlit_app.py
import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("summits_with_tags.csv")

# Tag descriptions (tooltip or label)
tag_labels = {
    1: "Drive up",
    2: "Public Transport",
    3: "Easy Walk (<30 mins)",
    4: "Moderate Walk (30-90 mins)",
    5: "Longer Walk (1.5 - 6 hrs)",
    6: "Overnight hike",
    7: "Potential Access Issues",
    8: "Drive up - 4WD",
    9: "Cycle Friendly",
    10: "Rock Climbing",
    11: "Disability Friendly",
    12: "Remote/Difficult Trailhead"
}

st.title("SOTA Summit Tag Explorer")

# Multi-select tag filter
selected_tags = st.multiselect(
    "Select tags to filter summits:",
    options=[(f"Tag_{i}", tag_labels[i]) for i in range(1, 13)],
    format_func=lambda x: tag_labels[int(x.split("_")[1])]
)

# Filter data
if selected_tags:
    filtered_df = df.copy()
    for tag_col in selected_tags:
        filtered_df = filtered_df[filtered_df[tag_col] == True]
    st.write(f"Showing {len(filtered_df)} summits with selected tags:")
    st.dataframe(filtered_df)
else:
    st.write("Select one or more tags to see matching summits.")

