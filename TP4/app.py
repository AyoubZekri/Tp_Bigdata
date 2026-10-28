
import os
import pandas as pd

DATA_FILE = os.getenv("DATA_FILE", "/app/data/traffic_data_2016.csv")
CHUNK_SIZE = 100_000


def main():
    print("=" * 60)
    print("TP04 - BIG DATA ANALYSIS WITH DOCKER")
    print("CHUNKED CSV READING")
    print("=" * 60)

    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    total_rows = 0
    total_missing = None
    numeric_sum = None
    numeric_count = None
    first_chunk = None
    columns = None

    print(f"\nDataset: {DATA_FILE}")
    print(f"Chunk size: {CHUNK_SIZE:,}")
    print("\nReading dataset in chunks...")

    for chunk_number, chunk in enumerate(
        pd.read_csv(DATA_FILE, chunksize=CHUNK_SIZE, low_memory=True),
        start=1
    ):
        if first_chunk is None:
            first_chunk = chunk.head()
            columns = chunk.columns.tolist()
            total_missing = pd.Series(0, index=columns, dtype="int64")
            numeric_sum = pd.Series(dtype="float64")
            numeric_count = pd.Series(dtype="int64")

        rows = len(chunk)
        total_rows += rows
        total_missing += chunk.isnull().sum()

        numeric = chunk.select_dtypes(include="number")
        sums = numeric.sum()
        counts = numeric.count()

        numeric_sum = numeric_sum.add(sums, fill_value=0)
        numeric_count = numeric_count.add(counts, fill_value=0)

        print(
            f"Processed chunk {chunk_number}: "
            f"{rows:,} rows | Total: {total_rows:,}"
        )

    if total_rows == 0:
        print("The dataset is empty.")
        return

    print("\n" + "=" * 60)
    print("ANALYSIS RESULTS")
    print("=" * 60)
    print(f"Total rows: {total_rows:,}")
    print(f"Total columns: {len(columns)}")
    print("\nColumn names:")
    print(columns)

    print("\nMissing values per column:")
    print(total_missing.to_string())

    print("\nNumeric column means:")
    means = numeric_sum.div(numeric_count.replace(0, pd.NA))
    print(means.to_string())

    print("\nFirst 5 rows:")
    print(first_chunk.to_string(index=False))

    print("\nAnalysis completed successfully.")


if __name__ == "__main__":
    main()
