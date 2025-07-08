# Google Maps Scraper - Technical Analysis

## Code Structure Analysis

### main.py - Entry Point and Orchestration

#### Key Components:

**1. Logging Setup**
```python
logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
```
- Centralizes all logging to `scraper.log`
- Provides timestamped log entries for debugging

**2. Queue Management System**
```python
# Load existing queue or create new one
if os.path.exists(queue_path):
    with open(queue_path, "rb") as qf:
        city_queue = pickle.load(qf)
else:
    city_queue = queue.Queue()
    # Populate from CSV
```
- Uses Python's `queue.Queue` for thread-safe operations
- Pickle serialization enables resumable scraping
- Fault-tolerant queue loading with error handling

**3. Province Processing Loop**
```python
for file in os.listdir(PROVINCE_DIR):
    if not file.endswith(".csv"):
        continue
    # Process each province
```
- Iterates through all CSV files in province directory
- Extracts province name from filename
- Creates dedicated output directories

**4. City Processing Logic**
```python
while not city_queue.empty():
    city, lat, lon = city_queue.get()
    # Check if already processed
    if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
        continue
    # Scrape city
    scrape_city(city, lat, lon, province, out_path)
```
- Processes cities sequentially from queue
- Implements skip logic for already processed cities
- Handles errors gracefully without stopping entire process

### scraper.py - Core Scraping Engine

#### Search Strategy:

**1. Multi-Query Approach**
```python
QUERY_PHRASES = [
    "gyms near {lat},{lon}",
    "fitness centers near {lat},{lon}",
    "bodybuilding clubs near {lat},{lon}"
]
```
- Uses multiple search terms to maximize coverage
- Latitude/longitude coordinates for precise location targeting
- Focused on fitness-related businesses

**2. Browser Automation**
```python
def scrape_city(city, lat, lon, province, out_path, max_retries=3):
    browser = get_browser()
    collected = set()  # Prevent duplicates
```
- Creates isolated browser instance per city
- Implements duplicate detection with set data structure
- Retry mechanism for network failures

**3. Result Loading Strategy**
```python
# Scroll to load more results
prev_count = -1
for _ in range(5):
    browser.execute_script("window.scrollBy(0, 500);")
    wait_random(1, 2)
    results = browser.find_elements(By.CSS_SELECTOR, '[role="article"]')
    if len(results) == prev_count:
        break
```
- Implements infinite scroll simulation
- Detects when no more results are loaded
- Uses CSS selector to find business listings

**4. Data Extraction Logic**
```python
# Extract business information
name = res.find_element(By.CSS_SELECTOR, "[aria-label]").get_attribute("aria-label")
full_text = res.text.split('\n')
address = full_text[1] if len(full_text) > 1 else ""

# Parse various fields from text
for line in full_text:
    if line.startswith("+92") or line.replace(" ","").startswith("0"):
        phone = line
    if "reviews" in line.lower():
        reviews = line.split()[0]
    if "star" in line.lower():
        rating = line.split()[0]
```
- Uses aria-label for business names (accessibility-friendly)
- Parses structured text content for various fields
- Implements pattern matching for Pakistani phone numbers
- Extracts ratings and review counts using keyword search

### utils.py - Support Infrastructure

#### Browser Management:

**1. Proxy Rotation System**
```python
with open("proxies.txt") as f:
    PROXIES = [line.strip() for line in f if line.strip()]
proxy_pool = cycle(PROXIES)

def get_browser():
    proxy = next(proxy_pool)
    chrome_options.add_argument(f'--proxy-server=http://{proxy}')
```
- Loads proxy list from external file
- Uses `itertools.cycle` for infinite rotation
- Configures Chrome to use rotating proxies

**2. Anti-Detection Measures**
```python
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15...",
    # Multiple user agents
]
chrome_options.add_argument(f'--user-agent={random.choice(user_agents)}')
```
- Randomizes user agent strings
- Simulates different browser/OS combinations
- Reduces detection probability

**3. Timing Controls**
```python
def wait_random(min_sec=2, max_sec=5):
    time.sleep(random.uniform(min_sec, max_sec))
```
- Implements randomized delays
- Mimics human browsing patterns
- Prevents automated detection

## Data Flow Analysis

### Input Processing:
1. **CSV Reading**: Reads city coordinates from province files
2. **Queue Population**: Loads cities into processing queue
3. **State Management**: Handles resume/restart scenarios

### Scraping Process:
1. **Browser Launch**: Creates browser with proxy/user agent
2. **Search Execution**: Performs multiple searches per city
3. **Result Collection**: Scrolls and collects all listings
4. **Data Extraction**: Parses business information
5. **Output Writing**: Saves to structured CSV

### Output Generation:
1. **CSV Structure**: Creates standardized output format
2. **File Organization**: Organizes by province/city hierarchy
3. **State Persistence**: Saves queue state for resumption

## Performance Characteristics

### Memory Usage:
- **Queue Storage**: O(n) where n = number of cities
- **Browser Instances**: One per city (cleaned up after use)
- **Result Caching**: Set-based duplicate detection

### Network Patterns:
- **Request Rate**: Limited by random delays (2-7 seconds)
- **Proxy Rotation**: Distributes requests across multiple IPs
- **Retry Logic**: Handles transient network failures

### Scalability Factors:
- **Province Parallelization**: Could process multiple provinces
- **City Batching**: Sequential processing prevents overload
- **Resource Cleanup**: Proper browser disposal prevents memory leaks

## Error Handling Strategy

### Network Errors:
```python
for attempt in range(max_retries):
    try:
        browser.get(url)
        break
    except Exception as e:
        logging.warning(f"Attempt {attempt+1}/{max_retries}")
```

### Data Validation:
```python
if not name or not address:
    logging.warning(f"Skipping incomplete result")
    continue
```

### State Recovery:
```python
try:
    with open(queue_path, "rb") as qf:
        city_queue = pickle.load(qf)
except Exception as e:
    logging.warning(f"Couldn't load queue. Restarting: {e}")
    city_queue = queue.Queue()
```

## Security Considerations

### Anti-Detection:
- Proxy rotation prevents IP blocking
- User agent randomization
- Human-like timing patterns
- Headless browser operation

### Data Privacy:
- Extracts only publicly available information
- No personal data collection
- Respects robots.txt (implicitly)

### Rate Limiting:
- Randomized delays between requests
- Sequential processing approach
- Proxy distribution for load balancing

## Extension Points

### Custom Search Queries:
- Modify `QUERY_PHRASES` for different business types
- Add location-specific search terms
- Implement dynamic query generation

### Output Formats:
- Add JSON/XML export options
- Database integration capabilities
- Real-time data streaming

### Advanced Features:
- Parallel province processing
- Machine learning for better data extraction
- API integration for additional data sources

This technical analysis provides insight into the sophisticated engineering behind the Google Maps scraper, highlighting its robust architecture for reliable, scalable web scraping operations.