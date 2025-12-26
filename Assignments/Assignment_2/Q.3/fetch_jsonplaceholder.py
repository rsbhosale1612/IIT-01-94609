# fetch_jsonplaceholder.py
import requests
import json
import pandas as pd
from pathlib import Path


API_URL = API_URL = "https://jsonplaceholder.typicode.com/users"
 

def fetch_data(url):
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()   
    return resp.json()        

def save_json(data, filepath):
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved JSON to {filepath}")

def save_csv(data, filepath):
    df = pd.DataFrame(data)
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"Saved CSV to {filepath}")

def main():
    try:
        print(f"Fetching data from {API_URL} ...")
        data = fetch_data(API_URL)

        save_json(data, "output/posts.json")

        save_csv(data, "output/posts.csv")

        print("First 3 records (sample):")
        for rec in data[:3]:
            print(rec)
    except requests.exceptions.HTTPError as e:
        print("HTTP error:", e)
    except requests.exceptions.RequestException as e:
        print("Network error:", e)
    except Exception as e:
        print("Unexpected error:", e)

if __name__ == "__main__":
    main()
