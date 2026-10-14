
import time
import psutil
import pandas as pd

FILE_PATH = "data/traffic_data_2016.csv"
CHUNK_SIZE = 200_000

process = psutil.Process()

total_rows = 0

start = time.perf_counter()
peak_ram = 0.0

print("Starting Pandas Chunking...")

for chunk in pd.read_csv(
    FILE_PATH,
    chunksize=CHUNK_SIZE
):

    total_rows += len(chunk)

    current_ram = (
        process.memory_info().rss / (1024 ** 3)
    )
    peak_ram = max(peak_ram, current_ram)

    if total_rows % 200_000 < CHUNK_SIZE:
        print("Rows processed:", total_rows)


elapsed = time.perf_counter() - start

print("\n--- Chunking Results ---")
print("Rows processed:", total_rows)
print("time:", round(elapsed, 2), "seconds")
print("RAM:", round(peak_ram, 2), "GB")
