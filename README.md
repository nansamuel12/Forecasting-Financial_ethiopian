# Ethiopia Financial Inclusion - Unified Data Format v2

## Key Design Principle

**Don't force interpretation onto data.**

The previous version made a mistake: it assigned events to pillars (e.g., "Telebirr Launch" → USAGE). This is **biased** because:
- Telebirr affects both ACCESS and USAGE
- Fayda affects ACCESS, GENDER, and TRUST
- The pillar assignment is an **interpretation**, not a fact

## The Correct Approach

| Record Type | `category` column | `pillar` column |
|-------------|-------------------|-----------------|
| `observation` | (empty) | **YES** - what dimension is measured |
| `target` | (empty) | **YES** - what dimension is the goal |
| `event` | **Event type** (policy, product_launch, etc.) | **(empty)** - no pre-assignment |
| `impact_link` | (empty) | **YES** - pillar of the affected indicator |

---

## How It Works

### Events are neutral
```csv
EVT_0001,,event,product_launch,,Telebirr Launch,...
```
- `category` = what type of event (product_launch)
- `pillar` = empty (no pre-interpretation)

### Impact links capture effects
```csv
IMP_0001,EVT_0001,impact_link,,ACCESS,...,ACC_OWNERSHIP,direct,increase,high,15,12,...
IMP_0003,EVT_0001,impact_link,,USAGE,...,USG_P2P_COUNT,direct,increase,high,25,6,...
```
- One event → multiple impact_links
- Each impact_link has a pillar (derived from the affected indicator)

### Query: "What affects ACCESS?"
```python
# Get all impact_links that affect ACCESS indicators
access_impacts = df[
    (df['record_type'] == 'impact_link') & 
    (df['pillar'] == 'ACCESS')
]

# Join to get event details
access_events = access_impacts.merge(
    df[df['record_type'] == 'event'],
    left_on='parent_id',
    right_on='record_id'
)
```

---

## Event Categories

| category | Description | Examples |
|----------|-------------|----------|
| `product_launch` | New product/service | Telebirr, M-Pesa |
| `market_entry` | New competitor | Safaricom Ethiopia |
| `policy` | Government strategy | NFIS-II |
| `regulation` | Regulatory directive | KYC rules |
| `infrastructure` | System deployment | Fayda, EthioPay |
| `partnership` | Integration | M-Pesa + EthSwitch |
| `milestone` | Achievement | P2P > ATM |
| `economic` | Macro shock | FX reform |
| `pricing` | Price change | Safaricom rate hike |

---

## Pillar Definitions (for observations only)

| pillar | Measures |
|--------|----------|
| `ACCESS` | Can people reach services? |
| `USAGE` | Are people using services? |
| `AFFORDABILITY` | Can people afford services? |
| `GENDER` | Gender gaps |
| `QUALITY` | Do services work reliably? |
| `TRUST` | Do people trust the system? |
| `DEPTH` | Beyond payments (savings, credit)? |

---

## Building the Models

### ACCESS Model
```python
# Target: ACCESS observations
Y = df[(df['record_type'] == 'observation') & (df['pillar'] == 'ACCESS')]

# Features: Events that affect ACCESS (via impact_links)
access_impacts = df[(df['record_type'] == 'impact_link') & (df['pillar'] == 'ACCESS')]

# Create event dummies from the events
events = df[df['record_type'] == 'event']
```

### USAGE Model
```python
# Target: USAGE observations
Y = df[(df['record_type'] == 'observation') & (df['pillar'] == 'USAGE')]

# Features: Events that affect USAGE (via impact_links)
usage_impacts = df[(df['record_type'] == 'impact_link') & (df['pillar'] == 'USAGE')]
```

---

## Data Entry Rules

### Adding an observation
```
record_type: observation
category: (leave empty)
pillar: ACCESS or USAGE or GENDER etc.
indicator_code: ACC_OWNERSHIP, USG_P2P_COUNT, etc.
```

### Adding an event
```
record_type: event
category: product_launch, policy, infrastructure, etc.
pillar: (leave empty - don't pre-assign!)
indicator: Event name
```

### Adding an impact link
```
record_type: impact_link
parent_id: The event ID (EVT_XXXX)
category: (leave empty)
pillar: The pillar of the affected indicator
related_indicator: The indicator code being affected
```

---

## Files

| File | Purpose |
|------|---------|
| `ethiopia_fi_unified_data.csv` | The data (72 records after enrichment) |
| `reference_codes.csv` | Valid codes for each field |
| `SCHEMA_DESIGN.md` | Detailed schema documentation |

---

## Project Structure

```
ethiopia-fi-forecast/
├── .github/workflows/     # CI/CD workflows
├── data/
│   ├── raw/               # Source datasets
│   └── processed/         # Analysis-ready data
├── notebooks/             # Jupyter notebooks for EDA
├── src/                   # Source code
├── dashboard/             # Dashboard application
├── tests/                 # Unit tests
├── models/                # Trained models
├── reports/
│   └── figures/           # Generated visualizations
└── requirements.txt       # Python dependencies
```

## Tasks Completed

- **Task 1:** Data Exploration and Enrichment
  - Added 23 impact links connecting events to indicators
  - Added 4 new observations and 2 new events
  - Dataset expanded from 43 to 72 records

- **Task 2:** Exploratory Data Analysis
  - Comprehensive EDA with 17 visualizations
  - 7 key insights documented
  - Data quality assessment completed

- **Task 3:** Event Impact Modeling
  - Event-indicator association matrix
  - Impact modeling function with temporal dynamics
  - Model validation against historical data

- **Task 4:** Forecasting Access and Usage
  - Trend regression models (linear and log)
  - Event-augmented forecasts for 2025-2027
  - Scenario analysis (optimistic, base, pessimistic)

- **Task 5:** Dashboard Development
  - Interactive Streamlit dashboard
  - Multiple pages: Overview, Trends, Forecasts, Inclusion Projections
  - At least 4 interactive visualizations

- **Task 6:** Refactoring & Testing
  - Refactored core utilities into `src/utils.py`
  - Added comprehensive unit tests for ID generation logic
  - Established testing framework using `pytest`

---

## Running the Dashboard

### Prerequisites

Install required dependencies:
```bash
pip install -r requirements.txt
```

### Starting the Dashboard

Navigate to the project root directory and run:
```bash
streamlit run dashboard/app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

### Dashboard Features

**Overview Page:**
- Key metrics summary cards (Account Ownership, Mobile Money, P2P/ATM Ratio)
- Growth rate highlights
- P2P/ATM crossover visualization

**Trends Page:**
- Interactive time series plots with date range selector
- Multi-indicator comparison
- Channel comparison view (P2P vs ATM)
- Data download functionality

**Forecasts Page:**
- Forecast visualizations with confidence intervals
- Model selection (Event-Augmented, Trend Only, Both)
- Key projected milestones
- Forecast tables

**Inclusion Projections Page:**
- Financial inclusion rate projections
- Progress toward 60% target visualization
- Scenario selector (Optimistic, Base, Pessimistic)
- Answers to consortium's key questions
- Projection data download

### Troubleshooting

If you encounter issues:
1. Ensure all dependencies are installed: `pip install -r requirements.txt`
2. Verify the data file exists: `data/raw/ethiopia_fi_unified_data_enriched.csv`
3. Check that you're running from the project root directory
4. For port conflicts, use: `streamlit run dashboard/app.py --server.port 8502`