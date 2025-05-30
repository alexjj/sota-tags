import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("summits_with_tags.csv")

# Define tag metadata
tags = {
    1: {"label": "Drive up", "icon": "car.png"},
    2: {"label": "Public Transport", "icon": "bus.png"},
    3: {"label": "Easy Walk", "icon": "walk.png"},
    4: {"label": "Moderate Walk", "icon": "walk_2.png"},
    5: {"label": "Longer Walk", "icon": "walking.png"},
    6: {"label": "Overnight Hike", "icon": "camping.png"},
    7: {"label": "Access Issues", "icon": "caution.png"},
    8: {"label": "Drive up - 4WD", "icon": "suv.png"},
    9: {"label": "Cycle Friendly", "icon": "mountain-bike.png"},
    10: {"label": "Rock Climbing", "icon": "climber.png"},
    11: {"label": "Disability Friendly", "icon": "disability.png"},
    12: {"label": "Remote Trailhead", "icon": "effort.png"},
}

# Build tag selection
tag_options = [f"Tag_{i}" for i in tags.keys()]
selected_tags = st.multiselect(
    "Select tags to filter summits:",
    options=tag_options,
    format_func=lambda x: tags[int(x.split("_")[1])]["label"]
)

# Start with all data
filtered_df = df.copy()

# Apply tag filters if selected
if selected_tags:
    for tag_col in selected_tags:
        filtered_df = filtered_df[filtered_df[tag_col] == True]

    st.write(f"Showing {len(filtered_df)} summits with selected tags:")
else:
    st.info("Select one or more tags to see matching summits and map.")


    # Show map
if selected_tags and not filtered_df.empty:
    st.map(filtered_df.rename(columns={"Latitude": "latitude", "Longitude": "longitude"}))

    # Prepare display table
    def icon_row(row):
        icons_html = ""
        for tag_id, tag_info in tags.items():
            if row.get(f"Tag_{tag_id}", False):
                icons_html += f'<img src="https://www.sotadata.org.uk/en/assets/icons/{tag_info["icon"]}" title="{tag_info["label"]}" width="32" height="32" style="margin:2px;">'
        return icons_html

    display_df = filtered_df.rename(columns={
        "SummitCode": "ID",
        "SummitName": "Name"
    })[["ID", "Name", "Points"]].copy()
    display_df["Tags"] = filtered_df.apply(icon_row, axis=1)

    # Show table with HTML
    st.write(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)

elif selected_tags and filtered_df.empty:
    st.warning("No summits match the selected tags.")
