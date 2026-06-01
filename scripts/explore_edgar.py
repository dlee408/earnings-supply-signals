import os
import requests
from dotenv import load_dotenv

load_dotenv()

SEC_USER_AGENT = os.getenv("SEC_USER_AGENT")
if not SEC_USER_AGENT:
    raise ValueError("SEC_USER_AGENT not found in environment variables")


# SEC requires a user agent with contact information
HEADERS = {"User-Agent": SEC_USER_AGENT}

# CIK = "0000320193"  # Apple Inc.
CIK = "0000006951"  # Applied Materials, Inc.
URL = f"https://data.sec.gov/submissions/CIK{CIK}.json"

response = requests.get(URL, headers=HEADERS, timeout=10)
response.raise_for_status()
data = response.json()

print(f"Company Name: {data.get('name')}")
print(
    f"Number of filings: {len(data.get('filings', {}).get('recent', {}).get('form', []))}"
)
print(
    f"Recent filing types: {data.get('filings', {}).get('recent', {}).get('form', [])[:20]}"
)  # Print the first 20 filing types

# URL for Form 8-K with exhibit 99.1
# https://www.sec.gov/ix?doc=/Archives/edgar/data/0000006951/000162828026007661/amat-20260212.htm
