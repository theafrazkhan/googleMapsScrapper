# Google Maps Scraper - Workflow Diagram

## System Architecture Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           Google Maps Scraper Workflow                          │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Input Data    │    │   Processing    │    │   Output Data   │
│                 │    │                 │    │                 │
│ Province CSVs   │───▶│  Main Process   │───▶│  Results CSVs   │
│ - Punjab        │    │  - Queue Mgmt   │    │  - By Province  │
│ - Sindh         │    │  - State Persist│    │  - By City      │
│ - Balochistan   │    │  - Error Handle │    │  - Structured   │
│ - KPK           │    │                 │    │                 │
│ - etc.          │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   City Queue    │
                       │   (Per Province)│
                       │                 │
                       │ ┌─────────────┐ │
                       │ │   Pickle    │ │
                       │ │ State File  │ │
                       │ │ (Resume)    │ │
                       │ └─────────────┘ │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Scraping Loop  │
                       │                 │
                       │ For each city:  │
                       │ 1. Get coords   │
                       │ 2. Launch browser│
                       │ 3. Search Google│
                       │ 4. Extract data │
                       │ 5. Save CSV     │
                       │ 6. Update queue │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Browser Setup  │
                       │                 │
                       │ ┌─────────────┐ │
                       │ │ Proxy Pool  │ │
                       │ │ - Rotate    │ │
                       │ │ - Load Bal  │ │
                       │ └─────────────┘ │
                       │                 │
                       │ ┌─────────────┐ │
                       │ │ User Agents │ │
                       │ │ - Random    │ │
                       │ │ - Varied    │ │
                       │ └─────────────┘ │
                       │                 │
                       │ ┌─────────────┐ │
                       │ │ Chrome Opts │ │
                       │ │ - Headless  │ │
                       │ │ - No-sandbox│ │
                       │ └─────────────┘ │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ Google Maps API │
                       │                 │
                       │ Search Queries: │
                       │ 1. "gyms near   │
                       │    {lat},{lon}" │
                       │ 2. "fitness     │
                       │    centers..."  │
                       │ 3. "bodybuilding│
                       │    clubs..."    │
                       │                 │
                       │ For each query: │
                       │ - Load page     │
                       │ - Scroll results│
                       │ - Extract info  │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ Data Extraction │
                       │                 │
                       │ Business Info:  │
                       │ • Name          │
                       │ • Address       │
                       │ • Phone         │
                       │ • Website       │
                       │ • Rating        │
                       │ • Reviews       │
                       │ • Coordinates   │
                       │ • Plus Code     │
                       │ • Business Type │
                       │ • Opening Hours │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   File Output   │
                       │                 │
                       │ results/        │
                       │ ├── punjab/     │
                       │ │   ├── lahore.csv│
                       │ │   └── karachi.csv│
                       │ ├── sindh/      │
                       │ │   └── ...     │
                       │ └── ...         │
                       │                 │
                       │ CSV Format:     │
                       │ Name,Address,   │
                       │ Phone,Website,  │
                       │ Rating,Reviews, │
                       │ Lat,Lon,Plus,   │
                       │ Tags,Hours,City │
                       └─────────────────┘
```

## Data Flow Details

### 1. Input Processing
- **Province CSVs**: Contains city names with lat/lon coordinates
- **Queue Creation**: Cities loaded into processing queues
- **State Persistence**: Pickle files enable resumable operations

### 2. Browser Management
- **Proxy Rotation**: Distributes requests across multiple IP addresses
- **User Agent Randomization**: Mimics different browsers/devices
- **Anti-Detection**: Random delays and human-like behavior patterns

### 3. Search Strategy
- **Multi-Query Approach**: 3 different search terms per city
- **Coordinate-Based**: Uses precise lat/lon for location targeting
- **Result Pagination**: Scrolls to load all available results

### 4. Data Extraction
- **DOM Parsing**: Extracts structured information from page elements
- **Pattern Recognition**: Identifies phone numbers, ratings, URLs
- **Duplicate Detection**: Prevents duplicate entries using sets

### 5. Output Generation
- **CSV Structure**: Standardized format with 12 columns
- **File Organization**: Hierarchical structure by province/city
- **Data Validation**: Filters incomplete or invalid entries

## Error Handling Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Network     │    │ Retry Logic │    │ Continue    │
│ Timeout     │───▶│ (3 attempts)│───▶│ Processing  │
└─────────────┘    └─────────────┘    └─────────────┘
                            │
                            ▼
                   ┌─────────────┐
                   │ Log Error & │
                   │ Skip City   │
                   └─────────────┘

┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Parse Error │    │ Log Warning │    │ Continue to │
│ (Business)  │───▶│ Skip Entry  │───▶│ Next Result │
└─────────────┘    └─────────────┘    └─────────────┘

┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Queue Load  │    │ Recreate    │    │ Resume from │
│ Failure     │───▶│ from CSV    │───▶│ Beginning   │
└─────────────┘    └─────────────┘    └─────────────┘
```

This workflow ensures robust, scalable scraping with comprehensive error handling and resume capabilities.