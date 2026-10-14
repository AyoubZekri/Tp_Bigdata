
import time
import psutil
import dask.dataframe as dd

FILE_PATH = "data/traffic_data_2016.csv"

process = psutil.Process()
start = time.perf_counter()
peak_ram = 0.0

print("Creating Dask DataFrame...")

ddf = dd.read_csv(
    FILE_PATH,
    blocksize="64MB"
)

print("Number of partitions:", ddf.npartitions)
print("Dask DataFrame created.")
print("No full computation has happened yet.")


print("Mean calculation graph created.")
print("Executing with compute()...")


elapsed = time.perf_counter() - start
peak_ram = process.memory_info().rss / (1024 ** 3)

print("\n--- Dask Results ---")
print("Execution time:", round(elapsed, 2), "seconds")
print("RAM at the end:", round(peak_ram, 2), "GB")
