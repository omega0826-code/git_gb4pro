import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Set encoding for plot Korean characters
import matplotlib.font_manager as fm

# This setting depends on OS. For Windows, usually 'Malgun Gothic'.
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

input_file = r'd:\git_gb4pro\crawling\gangnam\data\gangnam_reviews_FINAL_ALL.csv'
output_report = r'd:\git_gb4pro\crawling\gangnam\data\gangnam_reviews_FINAL_ALL_EDA_Report.md'

def generate_eda_report():
    print(f"Reading {input_file}...")
    try:
        # Using low_memory=False to suppress DtypeWarning for large files
        df = pd.read_csv(input_file, encoding='utf-8-sig', low_memory=False)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    print("Data loaded. Shape:", df.shape)
    
    # 1. Basic Info
    total_reviews = len(df)
    columns = list(df.columns)
    
    # 2. Missing Values
    missing_values = df.isnull().sum()
    
    # 3. Basic Stats for numerical
    # Usually rating is numerical
    numerical_stats = df.describe().to_markdown()
    
    # 4. Review Distribution by Year (if date column exists)
    # Check for date columns: 'date', 'created_at', 'review_date', etc.
    date_col = None
    possible_date_cols = ['date', 'review_date', 'created_at', 'reg_date']
    for col in possible_date_cols:
        if col in df.columns:
            date_col = col
            break
            
    year_dist_md = ""
    if date_col:
        print(f"Found date column: {date_col}")
        try:
            # Try to convert to datetime, errors='coerce' to handle mixed format
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            df['year'] = df[date_col].dt.year
            year_counts = df['year'].value_counts().sort_index()
            year_dist_md = year_counts.to_markdown()
        except Exception as e:
            year_dist_md = f"Error processing date column: {e}"
    else:
        year_dist_md = "No recognized date column found."

    # 5. Rating Distribution
    rating_dist_md = ""
    if 'rating' in df.columns:
        rating_dist_md = df['rating'].value_counts().sort_index().to_markdown()

    # Generate Markdown Report
    print("Generating report...")
    
    report_content = f"""# Gangnam Reviews FINAL ALL - EDA Report

**1. Overview**
*   **File:** `{os.path.basename(input_file)}`
*   **Total Records:** {total_reviews:,}
*   **Columns:** {', '.join(columns)}

**2. Missing Values**
```
{missing_values.to_markdown()}
```

**3. Numerical Statistics**
```
{numerical_stats}
```

**4. Review Distribution by Year**
*   **Date Column:** {date_col if date_col else 'Not Found'}
```
{year_dist_md}
```

**5. Rating Distribution**
```
{rating_dist_md}
```

**6. Sample Data (First 5 rows)**
```
{df.head().to_markdown()}
```
"""
    
    try:
        with open(output_report, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"Report saved to {output_report}")
    except Exception as e:
        print(f"Error saving report: {e}")

if __name__ == "__main__":
    generate_eda_report()
