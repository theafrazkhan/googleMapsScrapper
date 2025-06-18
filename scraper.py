### scraper.py
import csv
import os
from utils import get_browser, wait_random
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

QUERY_PHRASES = [
    "gyms near {lat},{lon}",
    "fitness centers near {lat},{lon}",
    "bodybuilding clubs near {lat},{lon}"
]

def scrape_city(city, lat, lon, province, out_path, max_retries=3):
    import logging
    browser = get_browser()
    collected = set()
    headers = [
        "Name", "Address", "Phone Number", "Website", "Rating", "Number of Reviews", "Latitude", "Longitude", "Plus Code", "Business Type/Tags", "Opening Hours", "City"
    ]
    # Write headers if file is new
    if not os.path.exists(out_path) or os.path.getsize(out_path) == 0:
        with open(out_path, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
    try:
        for query in QUERY_PHRASES:
            url = f"https://www.google.com/maps/search/{query.format(lat=lat, lon=lon)}"
            for attempt in range(max_retries):
                try:
                    browser.get(url)
                    wait_random(5, 7)
                    break
                except Exception as e:
                    logging.warning(f"[WARN] Timeout or error for {query} ({city}): {e}. Attempt {attempt+1}/{max_retries}")
                    if attempt == max_retries - 1:
                        logging.error(f"[ERROR] Failed to load {url} after {max_retries} attempts.")
                        return
            # Scroll to load more results
            prev_count = -1
            for _ in range(5):
                browser.execute_script("window.scrollBy(0, 500);")
                wait_random(1, 2)
                results = browser.find_elements(By.CSS_SELECTOR, '[role="article"]')
                if len(results) == prev_count:
                    # No more results loaded, wait 2.5 seconds before moving to next query
                    wait_random(2, 3)
                    break
                prev_count = len(results)
            results = browser.find_elements(By.CSS_SELECTOR, '[role="article"]')
            logging.info(f"[INFO] Found {len(results)} results for: {query} ({city})")
            with open(out_path, "a", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for res in results:
                    try:
                        name = res.find_element(By.CSS_SELECTOR, "[aria-label]").get_attribute("aria-label")
                        if name in collected:
                            continue
                        collected.add(name)
                        # Try to extract as much as possible
                        full_text = res.text.split('\n')
                        address = full_text[1] if len(full_text) > 1 else ""
                        phone = website = rating = reviews = plus_code = tags = hours = ""
                        # Try to extract more fields
                        for line in full_text:
                            if line.startswith("+92") or line.replace(" ","").startswith("0"):
                                phone = line
                            if "reviews" in line.lower():
                                reviews = line.split()[0]
                            if "star" in line.lower():
                                rating = line.split()[0]
                            if ".com" in line or line.startswith("http"):
                                website = line
                            if "+" in line and len(line) > 5 and line[0] == "+":
                                plus_code = line
                            if "open" in line.lower() or "close" in line.lower():
                                hours = line
                        # Tags/Business type
                        if len(full_text) > 2:
                            tags = full_text[2]
                        # Data validation: skip if name or address is empty
                        if not name or not address:
                            logging.warning(f"[WARN] Skipping incomplete result for {city}: {name}, {address}")
                            continue
                        writer.writerow([
                            name, address, phone, website, rating, reviews, lat, lon, plus_code, tags, hours, city
                        ])
                    except Exception as e:
                        logging.error(f"[ERROR] Failed to parse result for {city}: {e}")
                        continue
    finally:
        browser.quit()

