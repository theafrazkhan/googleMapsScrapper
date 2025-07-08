# Google Maps Scraper

A comprehensive web scraper designed to systematically collect gym and fitness center data from Google Maps across Pakistan's provinces and cities. This project uses Selenium with undetected Chrome driver to extract business information while implementing sophisticated anti-detection measures.

## 🚀 Quick Start

```bash
git clone https://github.com/theafrazkhan/googleMapsScrapper.git
cd googleMapsScrapper
pip install -r requirements.txt
python main.py
```

## 📋 How It Works

This scraper processes cities systematically:

1. **Loads city data** from CSV files in `province_list/`
2. **Creates processing queues** for each province 
3. **Launches browser instances** with proxy rotation
4. **Searches Google Maps** using multiple fitness-related queries
5. **Extracts business information** from search results
6. **Saves structured data** to CSV files organized by province/city

### Key Features

- ✅ **Resumable Operations**: Automatically resumes from interruptions
- ✅ **Anti-Detection**: Proxy rotation, user agent randomization, human-like delays
- ✅ **Fault Tolerant**: Continues despite individual city failures
- ✅ **Comprehensive Coverage**: Multiple search queries per city
- ✅ **Structured Output**: Standardized CSV format with business details

## 📊 Data Coverage

The scraper currently covers **148,857 cities** across Pakistan:

| Province | Cities |
|----------|--------|
| Punjab | 62,204 |
| Sindh | 36,084 |
| Khyber Pakhtunkhwa | 25,619 |
| Balochistan | 16,743 |
| Azad Kashmir | 4,720 |
| Gilgit-Baltistan | 2,940 |
| Islamabad | 547 |

## 🔧 Setup & Configuration

### Prerequisites
- Python 3.7+
- Chrome browser
- Proxy servers (recommended)

### Configuration Files

**`proxies.txt`** - Proxy server list:
```
username:password@167.71.141.183:3128
username:password@134.209.183.25:3128
```

**`province_list/`** - Input CSV files with format:
```csv
name,latitude,longitude
Lahore,31.5204,74.3587
Karachi,24.8607,67.0011
```

## 📈 Output Format

Each city generates a CSV file with columns:
- Name, Address, Phone Number, Website
- Rating, Number of Reviews
- Latitude, Longitude, Plus Code
- Business Type/Tags, Opening Hours, City

## 🛠️ Advanced Usage

### Custom Search Queries
Modify `QUERY_PHRASES` in `scraper.py`:
```python
QUERY_PHRASES = [
    "restaurants near {lat},{lon}",
    "hotels near {lat},{lon}",
    "shops near {lat},{lon}"
]
```

### Performance Tuning
- Adjust wait times in `utils.py` for speed vs. detection trade-offs
- Scale proxy pool for higher throughput
- Monitor resource usage for optimal performance

## 📚 Documentation

- **[PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md)** - Detailed system architecture
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Comprehensive usage instructions
- **[TECHNICAL_ANALYSIS.md](TECHNICAL_ANALYSIS.md)** - Code structure analysis

## 🎯 Demo

Run the demonstration to see how the system works:
```bash
python demo_how_it_works.py
```

## ⚠️ Important Notes

- **Large Scale**: Full scraping may take days/weeks for all provinces
- **Resource Intensive**: Requires stable internet and sufficient disk space
- **Rate Limiting**: Implements delays to respect Google's servers
- **Legal Compliance**: Extracts only publicly available information

## 🔍 Requirements

```
selenium
undetected-chromedriver
```

## 📝 License

This project is for educational and research purposes. Please respect Google's terms of service and rate limits when using this scraper.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**Note**: This scraper is designed for Pakistan's geographic data but can be adapted for other regions by updating the input CSV files and search queries.
