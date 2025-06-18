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
        try:
            with open(queue_path, "rb") as qf:
                city_queue = pickle.load(qf)
        except Exception as e:
            logging.warning(f"[QUEUE LOAD ERROR] Couldn't load queue for {province}. Restarting: {e}")
            city_queue = queue.Queue()
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
        try:
            with open(queue_path, "wb") as qf:
                pickle.dump(city_queue, qf)
        except Exception as e:
            logging.warning(f"[QUEUE SAVE ERROR] Couldn't save queue for {province}: {e}")

    # Province done, remove queue file
    if os.path.exists(queue_path):
        os.remove(queue_path)
