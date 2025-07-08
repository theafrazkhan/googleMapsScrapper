# Google Maps Scraper - Project Architecture

## Overview
This project is a comprehensive web scraper designed to collect gym and fitness center data from Google Maps across Pakistan's provinces and cities. It uses Selenium with undetected Chrome driver to systematically scrape business information while avoiding detection.

## System Architecture

### Core Components

#### 1. `main.py` - Orchestration Engine
- **Purpose**: Entry point that manages the overall scraping workflow
- **Key Functions**:
  - Iterates through province CSV files
  - Manages city queues using pickle for resumable scraping
  - Handles error recovery and state persistence
  - Coordinates calls to the scraper module

#### 2. `scraper.py` - Core Scraping Logic
- **Purpose**: Implements the actual web scraping functionality
- **Key Functions**:
  - Executes multiple search queries per city
  - Scrolls through Google Maps results
  - Extracts business information from page elements
  - Writes structured data to CSV files

#### 3. `utils.py` - Support Utilities
- **Purpose**: Provides browser management and anti-detection features
- **Key Functions**:
  - Creates browser instances with proxy rotation
  - Implements random user agent selection
  - Provides randomized wait times

### Data Flow

```
Input CSVs (province_list/) 
    ↓
City Queue Creation (pickle state)
    ↓
Google Maps Search (multiple queries per city)
    ↓
Result Extraction & Processing
    ↓
CSV Output (results/{province}/{city}.csv)
```

## Detailed Workflow

### 1. Initialization Phase
- Scans `province_list/` directory for CSV files
- Each CSV contains: city name, latitude, longitude
- Creates or loads existing queue state from pickle files

### 2. City Processing Loop
For each city in the queue:
- Checks if results already exist (skip if present)
- Initializes browser with proxy and user agent
- Executes multiple search queries
- Scrolls to load all available results
- Extracts business data
- Saves to individual CSV file
- Updates queue state

### 3. Search Strategy
The scraper uses three targeted queries per city:
```python
QUERY_PHRASES = [
    "gyms near {lat},{lon}",
    "fitness centers near {lat},{lon}",
    "bodybuilding clubs near {lat},{lon}"
]
```

### 4. Anti-Detection Measures
- **Proxy Rotation**: Cycles through proxy servers
- **User Agent Randomization**: Varies browser fingerprint
- **Random Wait Times**: Mimics human browsing patterns
- **Headless Operation**: Runs browser in background

### 5. Data Extraction
From each business listing, extracts:
- Name (from aria-label attribute)
- Address (from text content)
- Phone number (Pakistani format detection)
- Website URL
- Rating and review count
- Plus code (Google's location code)
- Business type/tags
- Opening hours
- Geographic coordinates

## File Structure

```
googleMapsScrapper/
├── main.py                 # Main orchestration script
├── scraper.py             # Core scraping logic
├── utils.py               # Browser utilities
├── requirements.txt       # Python dependencies
├── proxies.txt           # Proxy server list
├── province_list/        # Input CSV files
│   ├── punjab_cities.csv
│   ├── sindh_cities.csv
│   └── ...
└── results/              # Output directory (created at runtime)
    ├── {province}/
    │   ├── {city}.csv
    │   └── ...
    └── {province}_queue.pkl  # State files
```

## Key Features

### Resumable Operations
- Uses pickle files to save queue state
- Can resume from interruption without losing progress
- Skips already processed cities

### Error Handling
- Retry mechanisms for network failures
- Continues processing despite individual city failures
- Comprehensive logging for debugging

### Scalability
- Processes multiple provinces concurrently
- Queue-based architecture for efficient memory usage
- Modular design allows easy extension

## Output Format

Each city produces a CSV file with columns:
- Name
- Address  
- Phone Number
- Website
- Rating
- Number of Reviews
- Latitude
- Longitude
- Plus Code
- Business Type/Tags
- Opening Hours
- City

## Technical Requirements

### Dependencies
- Python 3.7+
- Selenium WebDriver
- undetected-chromedriver
- Chrome browser

### System Requirements
- Stable internet connection
- Proxy servers (for anti-detection)
- Sufficient disk space for results

## Configuration

### Proxy Setup
Edit `proxies.txt` with format:
```
username:password@ip:port
```

### Input Data
Place CSV files in `province_list/` with columns:
- name (city name)
- latitude (decimal degrees)
- longitude (decimal degrees)

This architecture provides a robust, scalable solution for systematic data collection from Google Maps while maintaining ethical scraping practices through rate limiting and anti-detection measures.