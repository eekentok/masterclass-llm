import pandas as pd

df = pd.read_csv("data/all_links.csv", header=None)
df.columns = ["url"]
links = df["url"].dropna().unique().tolist()
print(df.columns)
print(links)