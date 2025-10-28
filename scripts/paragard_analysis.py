#!/usr/bin/env python3
"""
Paragard IUD MDR Analysis
MDL No. 2974 - Filed December 16, 2020 (N.D. Georgia)
Checking for PREDICTIVE vs REVERSE pattern
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 10)

print("="*80)
print("PARAGARD IUD MDR ANALYSIS")
print("MDL No. 2974 - Filed December 16, 2020")
print("="*80)

# Fetch data from FDA API
print("\nFetching Paragard MDR data from FDA OpenFDA API...")
url = "https://api.fda.gov/device/event.json"
params = {
    "search": "device.brand_name:Paragard",
    "count": "date_received",
    "limit": 1000
}

response = requests.get(url, params=params)
data = response.json()

print(f"API Status: {response.status_code}")
print(f"Records found: {len(data['results'])}")

# Parse results
records = []
for item in data['results']:
    date_str = item['time']
    count = item['count']
    
    # Parse date (YYYYMMDD format)
    try:
        if len(date_str) == 8:
            date = pd.to_datetime(date_str, format='%Y%m%d')
        else:
            continue
        
        records.append({
            'date': date,
            'count': count
        })
    except Exception as e:
        print(f"Error parsing date {date_str}: {e}")
        continue

# Create DataFrame
df = pd.DataFrame(records)
df = df.sort_values('date')

print(f"\nTotal records parsed: {len(df)}")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
print(f"Total reports: {df['count'].sum()}")

# MDL filing date
mdl_date = pd.to_datetime('2020-12-16')

# Add before/after column
df['period'] = df['date'].apply(lambda x: 'Before MDL' if x < mdl_date else 'After MDL')

# Monthly aggregation
df['year_month'] = df['date'].dt.to_period('M')
monthly = df.groupby(['year_month', 'period'])['count'].sum().reset_index()
monthly['date'] = monthly['year_month'].dt.to_timestamp()
monthly = monthly.sort_values('date')

# Statistics
before_df = df[df['date'] < mdl_date]
after_df = df[df['date'] >= mdl_date]

total_before = before_df['count'].sum()
total_after = after_df['count'].sum()

print("\n" + "="*80)
print("BEFORE vs AFTER MDL FILING (December 16, 2020)")
print("="*80)
print(f"BEFORE MDL: {total_before} reports")
print(f"AFTER MDL: {total_after} reports")

# Get 6-month window before MDL
six_months_before = mdl_date - pd.DateOffset(months=6)
critical_window = df[(df['date'] >= six_months_before) & (df['date'] < mdl_date)]

print("\n" + "="*80)
print("6-MONTH WINDOW BEFORE MDL (Jun 2020 - Dec 2020)")
print("="*80)
print(f"Total reports in window: {critical_window['count'].sum()}")

if len(critical_window) > 0:
    critical_monthly = critical_window.groupby(critical_window['date'].dt.to_period('M'))['count'].sum()
    print("\nMonth-by-month breakdown:")
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for period, count in critical_monthly.items():
        month_name = month_names[period.month - 1]
        print(f"  {month_name} {period.year}: {count} reports")
else:
    print("No reports in 6-month window before MDL filing")

# Get 6-month window after MDL
six_months_after = mdl_date + pd.DateOffset(months=6)
after_window = df[(df['date'] >= mdl_date) & (df['date'] <= six_months_after)]

print("\n" + "="*80)
print("6-MONTH WINDOW AFTER MDL (Dec 2020 - Jun 2021)")
print("="*80)
print(f"Total reports in window: {after_window['count'].sum()}")

if len(after_window) > 0:
    after_monthly = after_window.groupby(after_window['date'].dt.to_period('M'))['count'].sum()
    print("\nMonth-by-month breakdown:")
    for period, count in after_monthly.items():
        month_name = month_names[period.month - 1]
        print(f"  {month_name} {period.year}: {count} reports")
else:
    print("No reports in 6-month window after MDL filing")

# Pattern determination
print("\n" + "="*80)
print("PATTERN ANALYSIS")
print("="*80)

if total_before > total_after:
    pattern = "DECLINING (unusual)"
    interpretation = "Reports declined after MDL - may indicate under-reporting or data lag"
elif total_after > total_before * 2:
    pattern = "REVERSE (awareness-driven)"
    interpretation = "MDL filing drove increased reporting through publicity"
else:
    pattern = "FLAT/NEUTRAL"
    interpretation = "No significant spike before or after MDL filing"

print(f"Pattern Type: {pattern}")
print(f"Interpretation: {interpretation}")
print(f"Ratio (After/Before): {total_after/max(total_before, 1):.2f}x")

# Visualization
fig, axes = plt.subplots(2, 2, figsize=(18, 12))
fig.suptitle('Paragard IUD - MDL Pattern Analysis\nMDL No. 2974 Filed: December 16, 2020', 
             fontsize=16, fontweight='bold')

# 1. Timeline plot
ax1 = axes[0, 0]
timeline_daily = df.groupby('date')['count'].sum().reset_index()
ax1.plot(timeline_daily['date'], timeline_daily['count'], marker='o', linewidth=2, markersize=6, color='steelblue')
ax1.axvline(mdl_date, color='red', linestyle='--', linewidth=3, label='MDL Filed (Dec 16, 2020)')
ax1.fill_between(timeline_daily['date'], timeline_daily['count'], 
                  where=(timeline_daily['date'] < mdl_date), alpha=0.3, color='yellow', label='Before MDL')
ax1.fill_between(timeline_daily['date'], timeline_daily['count'], 
                  where=(timeline_daily['date'] >= mdl_date), alpha=0.3, color='lightcoral', label='After MDL')
ax1.set_xlabel('Date', fontsize=12)
ax1.set_ylabel('Reports per Day', fontsize=12)
ax1.set_title('Daily MDR Timeline', fontsize=14, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 2. Before vs After comparison
ax2 = axes[0, 1]
periods = ['Before MDL\n(1997-2020)', 'After MDL\n(2020-2022)']
counts = [total_before, total_after]
colors = ['lightyellow', 'lightcoral']
bars = ax2.bar(periods, counts, color=colors, edgecolor='black', linewidth=2)
ax2.set_ylabel('Total Reports', fontsize=12)
ax2.set_title(f'Total Reports: Before vs After MDL\nPattern: {pattern}', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

for bar, count in zip(bars, counts):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(count)}', ha='center', va='bottom', fontweight='bold', fontsize=12)

# 3. Yearly distribution
ax3 = axes[1, 0]
df['year'] = df['date'].dt.year
yearly = df.groupby('year')['count'].sum().reset_index()
bars = ax3.bar(yearly['year'], yearly['count'], color='steelblue', alpha=0.7)

# Highlight 2020 (MDL year)
for i, row in yearly.iterrows():
    if row['year'] == 2020:
        bars[i].set_color('red')

ax3.set_xlabel('Year', fontsize=12)
ax3.set_ylabel('Total Reports', fontsize=12)
ax3.set_title('Annual Report Distribution (2020 MDL year highlighted)', fontsize=14, fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')

for i, row in yearly.iterrows():
    if row['count'] > 0:
        ax3.text(row['year'], row['count'], str(int(row['count'])), 
                ha='center', va='bottom', fontweight='bold', fontsize=9)

# 4. Pattern summary box
ax4 = axes[1, 1]
ax4.axis('off')

summary = f"""
PARAGARD IUD - PATTERN SUMMARY

Device: Paragard Copper IUD
MDL: No. 2974
Filed: December 16, 2020
Court: N.D. Georgia (Judge Leigh Martin May)

DATA SUMMARY:
• Total Reports: {df['count'].sum()}
• Date Range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}
• Before MDL: {total_before} reports
• After MDL: {total_after} reports
• Ratio: {total_after/max(total_before, 1):.2f}x

PATTERN: {pattern}

INTERPRETATION:
{interpretation}

KEY FINDING:
Very low volume reporting overall. 
Sporadic reports over 23+ years.
No dramatic spike pattern visible.

NOTE:
Low report volume makes pattern 
analysis less reliable. May indicate:
- Under-reporting
- Device type (implant) reporting lag
- Data collection issues
"""

ax4.text(0.1, 0.95, summary, transform=ax4.transAxes, fontsize=11,
         verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round,pad=1', facecolor='lightyellow', alpha=0.5, edgecolor='orange', linewidth=2))

plt.tight_layout()
plt.savefig('paragard_mdl_analysis.png', dpi=300, bbox_inches='tight')
print("\n" + "="*80)
print("Visualization saved: paragard_mdl_analysis.png")
print("="*80)

# Save detailed data
summary_data = {
    'Metric': [
        'Device',
        'MDL Number',
        'MDL Filed Date',
        'Court',
        'Total Reports',
        'Date Range Start',
        'Date Range End',
        'Reports Before MDL',
        'Reports After MDL',
        'Ratio (After/Before)',
        '6-Month Before Window',
        '6-Month After Window',
        'Pattern Type',
        'Interpretation'
    ],
    'Value': [
        'Paragard Copper IUD',
        'MDL No. 2974',
        '2020-12-16',
        'N.D. Georgia',
        df['count'].sum(),
        df['date'].min().strftime('%Y-%m-%d'),
        df['date'].max().strftime('%Y-%m-%d'),
        total_before,
        total_after,
        f"{total_after/max(total_before, 1):.2f}x",
        critical_window['count'].sum(),
        after_window['count'].sum(),
        pattern,
        interpretation
    ]
}

summary_df = pd.DataFrame(summary_data)

# Detailed timeline
timeline_df = df[['date', 'count', 'period']].copy()
timeline_df = timeline_df.sort_values('date')

with pd.ExcelWriter('paragard_mdl_analysis.xlsx', engine='openpyxl') as writer:
    summary_df.to_excel(writer, sheet_name='Summary', index=False)
    timeline_df.to_excel(writer, sheet_name='Timeline', index=False)
    yearly.to_excel(writer, sheet_name='Yearly', index=False)

print("Excel file saved: paragard_mdl_analysis.xlsx")
print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
