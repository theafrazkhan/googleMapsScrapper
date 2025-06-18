### utils.py
import random
import time
from itertools import cycle
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options

# Load proxies from file
with open("proxies.txt") as f:
    PROXIES = [line.strip() for line in f if line.strip()]
proxy_pool = cycle(PROXIES)

def get_browser():
    proxy = next(proxy_pool)
    print(f"[INFO] Using proxy: {proxy}")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f'--proxy-server=http://{proxy}')
    # Add random user agent
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0"
    ]
    chrome_options.add_argument(f'--user-agent={random.choice(user_agents)}')

    driver = uc.Chrome(options=chrome_options)
    driver.set_page_load_timeout(30)
    return driver

def wait_random(min_sec=2, max_sec=5):
    time.sleep(random.uniform(min_sec, max_sec))
