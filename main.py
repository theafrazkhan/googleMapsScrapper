"""
Context:

I'm building a full-scale Google Maps scraper using Python to create a directory of **every gym in Pakistan**. My input data lives in the `province_list/` folder — each CSV contains city names and their corresponding latitude and longitude. Each file is named after a province (e.g., punjab.csv, sindh.csv).

Goal:
- For each city, run at least 3 different query types on Google Maps (like `gyms near lat,lon`, `fitness centers near lat,lon`, etc.)
- Extract **all available details** from the Google Maps results:
  - name, address, phone, website, rating, review count, coordinates, plus code, tags, opening hours, and the city name itself

Architecture:
- I have 3 proxies (Squid servers) running on different DigitalOcean droplets. They are listed in `proxies.txt` in the format `user:pass@ip:port`.
- I want proxy rotation (round robin) to avoid detection and rate limiting.
- The script uses `undetected-chromedriver` + `selenium` to avoid being blocked.
- I want the results saved as individual CSVs: one per city, inside folders named after each province (e.g., `results/punjab/lahore.csv`).

Project structure:
gym_scraper/
├── province_list/        # Input: province_name.csv files (name, latitude, longitude)
├── results/              # Output: results/province_name/city.csv
├── proxies.txt           # 3 rotating proxies (used with Chrome)
├── requirements.txt      # Only selenium + undetected-chromedriver
├── main.py               # Loops over all cities and kicks off scraping
├── scraper.py            # Uses selenium to extract gym data
├── utils.py              # Handles proxy rotation + browser setup

I need Copilot to:
- Help expand or improve this architecture
- Optimize selenium usage for Google Maps search
- Improve proxy handling or failover
- Add scrolling + retry logic if needed
- Introduce delays, random user agents, and stealth settings
- Maintain light dependencies (no Scrapy, no heavy 3rd-party APIs)

Please respect this entire context when generating completions or code suggestions. Assume the intent is to **scrape every gym in Pakistan completely, without getting blocked**, and store them by province and city.
"""




### main.py
import os
import csv
import queue
import pickle
import logging
from scraper import scrape_city

# Setup logging
logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

PROVINCE_DIR = "province_list"
RESULTS_DIR = "results"

for file in os.listdir(PROVINCE_DIR):
    if not file.endswith(".csv"):
        continue

    province = file.replace(".csv", "")
    path = os.path.join(PROVINCE_DIR, file)
    queue_path = os.path.join(RESULTS_DIR, f"{province}_queue.pkl")
    if os.path.exists(queue_path):
        with open(queue_path, "rb") as qf:
            city_queue = pickle.load(qf)
    else:
        city_queue = queue.Queue()
        with open(path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                city = row["name"].strip()
                lat = row["latitude"].strip()
                lon = row["longitude"].strip()
                city_queue.put((city, lat, lon))

    out_dir = os.path.join(RESULTS_DIR, province)
    os.makedirs(out_dir, exist_ok=True)

    while not city_queue.empty():
        city, lat, lon = city_queue.get()
        out_path = os.path.join(out_dir, f"{city.lower().replace(' ', '_')}.csv")
        if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
            logging.info(f"[SKIP] {city}, {province} already scraped. Skipping.")
            continue
        logging.info(f"[START] Scraping {city}, {province}...")
        try:
            scrape_city(city, lat, lon, province, out_path)
            logging.info(f"[DONE] {city}, {province} successfully scraped.")
        except Exception as e:
            logging.error(f"[ERROR] Failed to scrape {city}, {province}: {e}")
        print(f"[✓] Done with {city}\n")
        # Save queue state after each city
        with open(queue_path, "wb") as qf:
            pickle.dump(city_queue, qf)
    # Province done, remove queue file
    if os.path.exists(queue_path):
        os.remove(queue_path)
