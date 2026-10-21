import os
import pandas as pd

SRC = r"D:\Master2\Big Data\TP2\data\traffic_data_2016.csv"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "traffic_sample_200k.csv")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

TARGET = 200_000
STEP = 677  

parts, offset = [], 0
for chunk in pd.read_csv(SRC, chunksize=5_000_000, low_memory=False):
    idx = range((-offset) % STEP, len(chunk), STEP)
    parts.append(chunk.iloc[list(idx)])
    offset += len(chunk)
    print("rows read:", offset, flush=True)

df = pd.concat(parts, ignore_index=True)
if len(df) > TARGET: 
    df = df.iloc[[int(i * len(df) / TARGET) for i in range(TARGET)]]
df.to_csv(OUT, index=False, encoding="utf-8-sig")

print("Rows:", len(df), "| sensors:", df["sensor_id"].nunique())
print("Dates:", df["entry_date"].min(), "->", df["entry_date"].max())
print("Output:", OUT)
