import pandas as pd
import requests
import time

# Load CSV
summits_df = pd.read_csv("uksummits.csv")

# Prepare tag columns
for tag_id in range(1, 13):
    summits_df[f"Tag_{tag_id}"] = False

# Loop through summits
for idx, row in summits_df.iterrows():
    summit_code = row['SummitCode']
    url = f"https://api-db2.sota.org.uk/summits/tags/{summit_code}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        tags = response.json()
        for tag in tags:
            tag_id = tag['TagID']
            active = tag['Active']
            summits_df.at[idx, f"Tag_{tag_id}"] = active
    except Exception as e:
        print(f"Failed to fetch tags for {summit_code}: {e}")

    time.sleep(0.2)  # Be kind to the API

# Save to new CSV
summits_df.to_csv("summits_with_tags.csv", index=False)
