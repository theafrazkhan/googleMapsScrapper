# Google Maps Scraper - Usage Guide

## Quick Start

### Prerequisites
1. Python 3.7 or higher
2. Chrome browser installed
3. Internet connection
4. Valid proxy servers (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/theafrazkhan/googleMapsScrapper.git
   cd googleMapsScrapper
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure proxies** (Optional but recommended)
   Edit `proxies.txt` with your proxy credentials:
   ```
   username:password@167.71.141.183:3128
   username:password@134.209.183.25:3128
   username:password@46.101.80.124:3128
   ```

4. **Prepare input data**
   Place CSV files in `province_list/` directory with format:
   ```csv
   name,latitude,longitude
   Lahore,31.5204,74.3587
   Karachi,24.8607,67.0011
   ```

### Running the Scraper

```bash
python main.py
```

The scraper will:
- Process each province CSV file
- Create a queue of cities to scrape
- Launch browser instances with proxy rotation
- Scrape gym data for each city
- Save results to `results/{province}/{city}.csv`

## Configuration Options

### Proxy Configuration
The scraper uses proxy rotation for anti-detection. Format in `proxies.txt`:
```
# Format: username:password@ip:port
proxyuser:proxypass@167.71.141.183:3128
```

### Search Query Customization
Edit `QUERY_PHRASES` in `scraper.py` to modify search terms:
```python
QUERY_PHRASES = [
    "gyms near {lat},{lon}",
    "fitness centers near {lat},{lon}",
    "bodybuilding clubs near {lat},{lon}"
]
```

### Browser Settings
Modify `get_browser()` in `utils.py` for browser options:
- Headless mode (default: enabled)
- User agent rotation
- Proxy settings
- Timeout values

## Understanding the Output

### File Structure
```
results/
├── punjab/
│   ├── lahore.csv
│   ├── faisalabad.csv
│   └── ...
├── sindh/
│   ├── karachi.csv
│   ├── hyderabad.csv
│   └── ...
└── punjab_queue.pkl (state file)
```

### CSV Format
Each city file contains:
| Column | Description | Example |
|--------|-------------|---------|
| Name | Business name | "Gold's Gym" |
| Address | Street address | "123 Main St, Lahore" |
| Phone Number | Contact number | "+92 42 1234567" |
| Website | Business website | "https://goldsgym.com" |
| Rating | Star rating | "4.5" |
| Number of Reviews | Review count | "150" |
| Latitude | Coordinates | "31.5204" |
| Longitude | Coordinates | "74.3587" |
| Plus Code | Google Plus Code | "9J2G+8Q Lahore" |
| Business Type/Tags | Category | "Gym" |
| Opening Hours | Schedule | "6 AM - 10 PM" |
| City | City name | "Lahore" |

## Monitoring and Debugging

### Log Files
The scraper creates `scraper.log` with detailed information:
- City processing status
- Error messages
- Network timeouts
- Queue state changes

### Console Output
Real-time progress indicators:
```
[INFO] Using proxy: proxyuser:proxypass@167.71.141.183:3128
[START] Scraping Lahore, Punjab...
[INFO] Found 25 results for: gyms near 31.5204,74.3587 (Lahore)
[DONE] Lahore, Punjab successfully scraped.
[✓] Done with Lahore
```

### Error Handling
Common issues and solutions:

1. **Proxy Connection Failed**
   - Check proxy credentials
   - Verify proxy server status
   - Try different proxy

2. **Browser Timeout**
   - Increase timeout in `utils.py`
   - Check internet connection
   - Reduce concurrent operations

3. **No Results Found**
   - Verify city coordinates
   - Check search queries
   - Ensure Google Maps accessibility

## Resume Interrupted Scraping

The scraper automatically resumes from where it left off:
- Queue state saved in `.pkl` files
- Skips already processed cities
- Continues with remaining cities

To force restart:
```bash
rm results/*_queue.pkl
python main.py
```

## Performance Optimization

### Speed vs. Detection Trade-offs
- **Faster**: Reduce wait times in `wait_random()`
- **Safer**: Increase delays, use more proxies
- **Balanced**: Default settings (recommended)

### Resource Usage
- Memory: ~100MB per browser instance
- Storage: ~1-10MB per city (depends on results)
- Network: Continuous during operation

### Scaling Considerations
- One browser instance per city
- Proxy rotation prevents IP blocking
- Consider rate limiting for large datasets

## Troubleshooting

### Common Issues

1. **Chrome Driver Not Found**
   ```bash
   # Install Chrome browser
   sudo apt-get install google-chrome-stable
   ```

2. **Import Errors**
   ```bash
   # Reinstall dependencies
   pip install --upgrade -r requirements.txt
   ```

3. **Permission Denied**
   ```bash
   # Check file permissions
   chmod +x main.py
   ```

4. **Network Issues**
   - Verify proxy connectivity
   - Check firewall settings
   - Test with different proxy

### Best Practices

1. **Use Quality Proxies**
   - Residential proxies preferred
   - Rotate frequently
   - Test before use

2. **Monitor Resource Usage**
   - Watch CPU/memory consumption
   - Monitor disk space
   - Check network bandwidth

3. **Respect Rate Limits**
   - Don't reduce wait times too much
   - Use reasonable batch sizes
   - Monitor for blocking

4. **Data Validation**
   - Check output quality
   - Verify coordinate accuracy
   - Validate business information

## Advanced Usage

### Custom Search Queries
Modify search patterns for different business types:
```python
QUERY_PHRASES = [
    "restaurants near {lat},{lon}",
    "hotels near {lat},{lon}",
    "shops near {lat},{lon}"
]
```

### Parallel Processing
For large datasets, consider:
- Running multiple instances
- Different provinces in parallel
- Separate proxy pools

### Data Post-Processing
After scraping, you might want to:
- Merge CSV files
- Clean and validate data
- Remove duplicates
- Geocode addresses

This guide provides comprehensive instructions for using the Google Maps scraper effectively while maintaining ethical scraping practices.