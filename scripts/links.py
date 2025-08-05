import csv
import pandas as pd
import numpy as np

'''
This script is used to append new links to the combined_links.csv file.

- Read combined_links.csv
- Read new_links.txt
- Create a new csv file with the new links named new_links.csv
- Check if the new links are already in the combined_links.csv
- If they are not, append them to the new_links.csv
- Save the result to new_links.csv
- Append the new_links.csv to the combined_links.csv
- Print the result
'''

# Read the existing combined links
df = pd.read_csv("data/input/combined_links.csv", header=None, names=["link"])

# Read new links from new_links.txt (one link per line)
with open("data/input/new_links.txt", "r") as f:
    new_links = [line.strip() for line in f if line.strip()]

# Convert to DataFrame
df_new = pd.DataFrame(new_links, columns=["link"])

# Find links that are not already in the combined file
existing_links = set(df["link"].tolist())
new_unique_links = df_new[~df_new["link"].isin(existing_links)]

# Save new unique links to new_links.csv
new_unique_links.to_csv("data/input/new_links.csv", index=False, header=False)

# Concatenate and drop duplicates
df_combined = pd.concat([df, df_new], ignore_index=True).drop_duplicates().reset_index(drop=True)

# Save back to combined_links.csv
df_combined.to_csv("data/input/combined_links.csv", index=False, header=False)

# Print the result
print("Combined links:")
print(df_combined)
print(f"\nNew unique links saved to new_links.csv: {len(new_unique_links)} links")