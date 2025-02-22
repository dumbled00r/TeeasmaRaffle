import asyncio
import csv

from curl_cffi.requests import AsyncSession

session = AsyncSession(
    impersonate="chrome120",
    headers={
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://dune.com",
        "referer": "https://dune.com/",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    },
)

API_URL = "https://core-api.dune.com/public/execution"


async def fetch_data(offset: int, limit: int = 1000):
    response = await session.post(
        API_URL,
        json={
            "execution_id": "01JMNT6FRS3YNZDNKJG4JBHC4T",
            "query_id": 4760011,
            "parameters": [],
            "pagination": {"limit": limit, "offset": offset},
        },
    )
    return response.json().get("execution_succeeded", {}).get("data", [])


async def collect_data():
    all_data = []
    limit = 1000
    total_records = 1000

    for offset in range(0, total_records, limit):
        print(f"Fetching data with offset {offset}...")
        batch = await fetch_data(offset, limit)
        if not batch:
            break
        all_data.extend(batch)

    return all_data


def save_to_csv(data, filename="data.csv"):
    if not data:
        print("No data to save!")
        return

    fieldnames = data[0].keys()

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"Data successfully saved to {filename}")


async def main():
    data = await collect_data()
    save_to_csv(data)


if __name__ == "__main__":
    asyncio.run(main())
