# BROWSING BEHAVIOR ANALYSIS
    

# Browsing History Data Analysis - Powr of You Assignment

## 📋 Project Overview

Analyze the browsing history dataset to uncover patterns, derive insights, and present findings through clear visualizations. Your task includes cleaning and preprocessing the data, exploring trends in user behavior, identifying key metrics, and crafting a compelling data-driven story. Use Python (and Power BI if you want) to create at least 5 pieces of analysis and visualizations that effectively communicate your insights. We are evaluating your analytical thinking, problem-solving approach, coding quality, and ability to present actionable insights in a structured report.

## 🎯 Assignment Objectives

- Explore and clean browsing history dataset
- Analyze patterns in user behavior
- Extract meaningful insights and trends
- Create 5+ compelling visualizations
- Generate actionable recommendations
- Present findings in a structured report

## 📁 Project Structure

```
browsing-history-analysis/
│
├── dataset/
│   └── py_demo_client_extension_30_20250221075805in.csv
│
├── main.ipynb              # Initial exploration and rough work
├── main.py                 # Final analysis script (comprehensive)
├── requirements.txt        # Project dependencies
├── README.md              # This file
│
├── output/                 # Generated after running analysis
│   ├── cleaned_browsing_data.csv
│   ├── powerbi_domain_summary.csv
│   ├── powerbi_time_summary.csv
│   ├── powerbi_category_summary.csv
│   └── executive_summary.md
│
└── images/         # Saved plots and charts
    
```

## 🛠️ Prerequisites

- Python 3.8 or higher
- `uv` package manager installed ([Installation Guide](https://github.com/astral-sh/uv))

## 🚀 Installation & Setup

### 1. Clone or Download the Project
```bash
# If using git
git clone https://github.com/mitangshu/powr-browsing-history-analysis.git
cd powr-browsing-history-analysis

# Or download and extract the project files
```

### 2. Create Virtual Environment with uv
```bash
# Create a new virtual environment
uv venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
# Install all required packages
uv pip install -r requirements.txt

# Or install packages individually:
uv pip install pandas numpy matplotlib seaborn plotly jupyter
```

### 4. Verify Installation
```bash
# Check if all packages are installed correctly
uv pip list
```

## 📊 Required Dependencies

The project uses the following Python packages:

```txt
pandas>=1.5.0
numpy>=1.24.0
matplotlib>=3.6.0
seaborn>=0.12.0
plotly>=5.0.0
jupyter>=1.0.0
ipykernel>=6.0.0
```

## 🎮 Usage Instructions

### Option 1: Run Complete Analysis (Recommended)
```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# Run the main analysis script
python main.py
```

### Option 2: Jupyter Notebook Exploration
```bash
# Start Jupyter Notebook
jupyter notebook

# Open main.ipynb for initial exploration and rough work
# The notebook contains step-by-step analysis process
```

### Option 3: Interactive Python Session
```python
# Import the analyzer class
from main import BrowsingDataAnalyzer

# Initialize analyzer with dataset path
analyzer = BrowsingDataAnalyzer('dataset/py_demo_client_extension_30_20250221075805in.csv')

# Run complete analysis
data, insights = analyzer.run_complete_analysis()

# Access specific analysis results
print(insights['top_domains'])
print(insights['time_patterns'])
```

## 📈 Analysis Components

The analysis includes the following components:

### 1. Data Loading & Cleaning
- Extracts browsing data from CSV file
- Removes invalid/incomplete records
- Converts timestamps to proper datetime format
- Enriches data with additional features (domain, category, etc.)

### 2. Behavioral Analysis
- **Top Domains**: Most frequently visited websites
- **Time Patterns**: Peak browsing hours and daily trends
- **Category Analysis**: Website categorization and usage patterns
- **Navigation Patterns**: Transition types and user flow
- **Session Analysis**: Browsing session identification and characteristics

### 3. Visualizations Created
1. **Top Domains Bar Chart** - Most visited websites
2. **Hourly Activity Line Plot** - Browsing patterns by hour
3. **Category Pie Chart** - Website category distribution
4. **Daily Activity Heatmap** - Activity intensity over time
5. **Session Length Distribution** - Histogram and box plot analysis

### 4. Insights & Recommendations
- Key behavioral patterns identified
- Actionable recommendations provided
- Executive summary for stakeholders
- Business implications highlighted

## 📄 File Descriptions

### Core Files
- **`main.py`**: Complete analysis script with BrowsingDataAnalyzer class
- **`main.ipynb`**: Jupyter notebook for initial exploration and rough work
- **`dataset/py_demo_client_extension_30_20250221075805in.csv`**: Raw browsing history data

### Generated Output Files
- **`cleaned_browsing_data.csv`**: Processed and cleaned dataset
- **`powerbi_*.csv`**: Summary tables for Power BI dashboard creation
- **`executive_summary.md`**: Business-focused summary of findings

## Key Metrics:
- Total browsing records: 5,099
- Unique domains visited: 409
- Analysis period: 31 days
- Average visits per day: 164.5
- Average sessions per day: 8.6
- Primary activity: Search (33.7% of browsing)
- Peak browsing time: 5:00 (498 visits)
- Most visited site: google.com (26.0% of total visits)
- Average session length: 19.1 page views

## Key Findings:
- **High Search Activity**: 26% of browsing time spent on Google searches
- **Professional Focus**: Strong usage of freelancing platforms (Upwork, Wellfound)
- **Work-Focused Timing**: Peak activity during business hours (9-11 AM)
- **Diverse Interests**: Balanced usage across multiple categories


