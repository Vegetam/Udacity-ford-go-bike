# Ford GoBike System Data — Exploratory & Explanatory Analysis
**Udacity Data Analyst Nanodegree — Project: Data Visualization**

---

## Project Overview

This project uses Python data visualization libraries to systematically explore the **Ford GoBike bike-sharing dataset** for February 2019, covering the greater San Francisco Bay Area. It follows the **Exploratory → Explanatory** pipeline:

- **Part I** — Exploratory Data Analysis: Systematic univariate → bivariate → multivariate investigation
- **Part II** — Explanatory Data Analysis: Polished presentation of the 3 most important findings

---

## Dataset

| Property | Value |
|---|---|
| Source | [Ford GoBike System Data](https://www.fordgobike.com/system-data) |
| Period | February 2019 |
| Raw rows | 183,412 trips |
| Cleaned rows | ~182,803 trips |
| Features | 16 original + 6 engineered |

**Key features:** `duration_sec`, `start_time`, `end_time`, `start/end_station_*`, `bike_id`, `user_type`, `member_birth_year`, `member_gender`, `bike_share_for_all_trip`

---

## Project Structure

```
fordgobike_repo/
│
├── data/
│   └── fordgobike_2019_02.csv       # Extracted from provided .7z archive
│
├── figures/                          # All generated visualizations (PNG)
│   ├── hist_duration.png
│   ├── bar_categorical.png
│   ├── bar_hourly.png
│   ├── scatter_age_duration.png
│   ├── box_duration.png
│   ├── bar_duration_day.png
│   ├── heatmap_hour_day.png
│   ├── facet_duration_gender_usertype.png
│   ├── facet_hourly_usertype.png
│   ├── scatter_multivariate.png
│   ├── explanatory_1_duration_usertype.png
│   ├── explanatory_2_hourly_patterns.png
│   └── explanatory_3_duration_gender_usertype.png
│
├── notebooks/
│   ├── Part_I_exploration.ipynb      # Exploratory analysis notebook
│   └── Part_II_explanatory.ipynb     # Explanatory analysis notebook

├── requirements.txt                  # Python dependencies
├── scripts/
│   ├── validate_project.py           # Smoke test used by CI
│   └── export_notebooks.py           # Executes notebooks and regenerates HTML/PDF
├── .github/workflows/
│   └── ci.yml                        # GitHub Actions workflow
├── Part_I_exploration.html           # Auto-generated HTML export of Part I
├── Part_II_explanatory.html          # Auto-generated HTML export of Part II
├── Part_I_exploration.pdf            # Auto-generated PDF export of Part I
├── Part_II_explanatory.pdf           # Auto-generated PDF export of Part II
└── README.md
```

---

## How to Run

### Prerequisites

```bash
pip install -r requirements.txt
```

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/fordgobike-analysis.git
cd fordgobike-analysis

# 2. Run the notebooks locally
jupyter notebook notebooks/Part_I_exploration.ipynb
jupyter notebook notebooks/Part_II_explanatory.ipynb

# 3. Regenerate submission exports locally (HTML + PDF)
python scripts/export_notebooks.py
```

### Automatic GitHub exports

Every push now triggers GitHub Actions to:

- pull the LFS-tracked dataset
- validate the dataset and notebook files
- execute both notebooks
- regenerate the HTML and PDF reports in the repo root
- overwrite old exports with the latest versions
- upload those files as workflow artifacts
- commit refreshed exports back to the branch automatically

---

## Key Findings

### Finding 1: Subscribers Take Short Commutes, Customers Take Leisure Rides
- Subscriber median trip duration: **8.2 minutes**
- Customer median trip duration: **13.2 minutes** (+61%)
- Customer distribution is flatter and wider, indicating exploratory usage

### Finding 2: Subscribers Are Commuters on Weekdays, Tourists on Weekends
- On weekdays, Subscribers show twin rush-hour spikes at **8 AM and 5 PM**
- On weekends, Subscriber behavior shifts to a **single midday peak** — matching the Customer pattern
- Customers show consistent midday usage all 7 days

### Finding 3: User Type Dominates Gender in Predicting Trip Duration
- Across all genders, the Customer–Subscriber gap is a consistent **~5 minutes**
- Gender differences within each user type are modest (<2 min)
- Female Customers have the longest median trips (~14.0 min)

---

## Visualizations Checklist (Rubric)

| Visualization Type | Plot | Location |
|---|---|---|
| ✅ Histogram | Trip duration distribution | Part I — 1.1 |
| ✅ Bar chart / Count plot | User type, gender, equity program | Part I — 1.2 |
| ✅ Scatter plot | Age vs. trip duration | Part I — 2.1 |
| ✅ Box plot | Duration by user type and gender | Part I — 2.2 |
| ✅ Clustered bar chart | Duration by day of week | Part I — 2.3 |
| ✅ Heatmap | Trips by hour × day of week | Part I — 2.4 |
| ✅ Facet plot | Duration by gender & user type | Part I — 3.1 |
| ✅ Facet plot (additional) | Hourly patterns by user type | Part I — 3.2 |
| ✅ Scatter with multiple encodings | Age vs. duration, color+shape | Part I — 3.3 |
| ✅ Polished explanatory viz 1 | Duration distribution comparison | Part II — Finding 1 |
| ✅ Polished explanatory viz 2 | Hourly patterns facet | Part II — Finding 2 |
| ✅ Polished explanatory viz 3 | Clustered bar w/ error bars | Part II — Finding 3 |

---

## Libraries Used

- **NumPy** — numerical operations
- **Pandas** — data loading and wrangling
- **Matplotlib** — low-level plotting
- **Seaborn** — statistical visualizations and FacetGrid

---

## Author

Udacity Data Analyst Nanodegree Project — Data Visualization


## Important Git setup for the large CSV

This repo includes `.gitattributes` so `data/fordgobike_2019_02.csv` is tracked with Git LFS. On a new machine, run:

```bash
git lfs install
```

Then add/commit/push normally. If you previously committed the CSV without LFS, rewrite history or start from a fresh repo before pushing.
