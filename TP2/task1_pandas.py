
import time
import psutil
import pandas as pd

FILE_PATH = "data/traffic_data_2016.csv"

process = psutil.Process()
start = time.perf_counter()

print("loading...")

try:
    df = pd.read_csv(FILE_PATH)

    elapsed = time.perf_counter() - start

    print("Loading successful.")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))
    print("time:", round(elapsed, 2), "seconds")
    print(
        "Current process RAM:",
        round(process.memory_info().rss / (1024 ** 3), 2),
        "GB"
    )


except MemoryError as error:
    print("Error:", error)

except Exception as error:
    print("Error:", repr(error))
