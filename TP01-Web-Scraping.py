import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://quotes.toscrape.com"

all_quotes = []

page_number = 1

while True:

    url = f"{BASE_URL}/page/{page_number}/"

    print(f"Scraping page {page_number}: {url}")

    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    if response.status_code != 200:
        print("Error:", response.status_code)
        break

    print("\n===== HTML SOURCE CODE =====")
    print(response.text[:2000])
    print("============================\n")

   
    soup = BeautifulSoup(response.text, "html.parser")

    quotes = soup.find_all("div", class_="quote")

    if not quotes:
        print("No more quotes found.")
        break

    for quote in quotes:

        text = quote.find(
            "span",
            class_="text"
        ).get_text(strip=True)

        author = quote.find(
            "small",
            class_="author"
        ).get_text(strip=True)

        tags = [
            tag.get_text(strip=True)
            for tag in quote.find_all("a", class_="tag")
        ]

        all_quotes.append({
            "Quote": text,
            "Author": author,
            "Tags": ", ".join(tags),
            "Page": page_number
        })

    page_number += 1

    time.sleep(0.5)


df = pd.DataFrame(all_quotes)

df.to_csv(
    "quotes.csv",
    index=False,
    encoding="utf-8-sig"
)


print("\n================================")
print("Scraping completed!")
print("Total quotes:", len(df))
print("CSV file: quotes.csv")
print("================================")

if len(df) >= 1000:
    print("SUCCESS: CSV 1000 rows.")
else:
    print("WARNING:1000 rows.")