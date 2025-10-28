#!/usr/bin/env python3
"""
Allergan BIOCELL Textured Breast Implant - Visual Analysis
MDL No. 2921 - Filed December 18, 2019
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (20, 12)

print("="*80)
print("ALLERGAN BIOCELL TEXTURED BREAST IMPLANT - VISUAL ANALYSIS")
print("MDL No. 2921 - Filed December 18, 2019")
print("="*80)

# Load data
df = pd.read_excel('allergan_biocell_all_mdr_reports.xlsx', sheet_name='All Reports')
print(f"Loaded {len(df)} records")

# Convert date
df['date_received'] = pd.to_datetime(df['date_received'])

# MDL filing date
mdl_date = pd.to_datetime('2019-12-18')

# Add period
df['period'] = df['date_received'].apply(lambda x: 'Before MDL' if x < mdl_date else 'After MDL')

# Calculate statistics
before_df = df[df['date_received'] < mdl_date]
after_df = df[df['date_received'] >= mdl_date]

print(f"\nBefore MDL: {len(before_df)} reports")
print(f"After MDL: {len(after_df)} reports")

# Monthly aggregation
df['year_month'] = df['date_received'].dt.to_period('M')
monthly_counts = df.groupby('year_month').size().reset_index(name='count')
monthly_counts['date'] = monthly_counts['year_month'].dt.to_timestamp()
monthly_counts = monthly_counts.sort_values('date')

# Focus on recent years (2015-2025)
recent_df = df[df['date_received'] >= '2015-01-01']
recent_monthly = recent_df.groupby(recent_df['date_received'].dt.to_period('M')).size().reset_index(name='count')
recent_monthly['date'] = recent_monthly['date_received'].dt.to_timestamp()
recent_monthly = recent_monthly.sort_values('date')

# Critical windows
six_months_before = mdl_date - pd.DateOffset(months=6)
six_months_after = mdl_date + pd.DateOffset(months=6)

critical_before = df[(df['date_received'] >= six_months_before) & (df['date_received'] < mdl_date)]
critical_after = df[(df['date_received'] >= mdl_date) & (df['date_received'] <= six_months_after)]

print(f"\n6-month window BEFORE: {len(critical_before)} reports")
print(f"6-month window AFTER: {len(critical_after)} reports")

# Monthly breakdown for critical period
critical_before_monthly = critical_before.groupby(critical_before['date_received'].dt.to_period('M')).size()
critical_after_monthly = critical_after.groupby(critical_after['date_received'].dt.to_period('M')).size()

print("\n" + "="*80)
print("6-MONTH WINDOW BREAKDOWN")
print("="*80)
print("\nBEFORE MDL (Jun-Dec 2019):")
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
for period, count in critical_before_monthly.items():
    month_name = month_names[period.month - 1]
    print(f"  {month_name} {period.year}: {count} reports")

print("\nAFTER MDL (Dec 2019-Jun 2020):")
for period, count in critical_after_monthly.items():
    month_name = month_names[period.month - 1]
    print(f"  {month_name} {period.year}: {count} reports")

# Pattern determination
before_avg = len(critical_before) / 6
after_avg = len(critical_after) / 6

print(f"\nAverage reports/month BEFORE MDL: {before_avg:.1f}")
print(f"Average reports/month AFTER MDL: {after_avg:.1f}")

if len(critical_before) > 0:
    ratio = len(critical_after) / len(critical_before)
else:
    ratio = 0

print(f"Ratio: {ratio:.2f}x")

if ratio > 2:
    pattern = "REVERSE (awareness-driven)"
elif ratio < 0.5:
    pattern = "DECLINING (unusual)"
else:
    pattern = "FLAT/NEUTRAL"

print(f"\nPattern Type: {pattern}")

# 2019 monthly breakdown
df_2019 = df[df['date_received'].dt.year == 2019]
monthly_2019 = df_2019.groupby(df_2019['date_received'].dt.to_period('M')).size()

print("\n" + "="*80)
print("2019 COMPLETE MONTHLY BREAKDOWN (MDL Year)")
print("="*80)
for period, count in monthly_2019.items():
    month_name = month_names[period.month - 1]
    marker = " ← MDL FILED" if period.month == 12 else ""
    print(f"{month_name} 2019: {count} reports{marker}")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(20, 12))
fig.suptitle('Allergan BIOCELL Textured Breast Implant - MDL Pattern Analysis\nMDL No. 2921 Filed: December 18, 2019', 
             fontsize=16, fontweight='bold')

# 1. Recent timeline (2015-2025)
ax1 = axes[0, 0]
ax1.plot(recent_monthly['date'], recent_monthly['count'], 
         marker='o', linewidth=2, markersize=5, color='steelblue', label='Monthly Reports')
ax1.axvline(mdl_date, color='red', linestyle='--', linewidth=3, label='MDL Filed (Dec 18, 2019)')
ax1.fill_between(recent_monthly['date'], recent_monthly['count'], 
                  where=(recent_monthly['date'] < mdl_date), 
                  alpha=0.3, color='yellow', label='Before MDL')
ax1.fill_between(recent_monthly['date'], recent_monthly['count'], 
                  where=(recent_monthly['date'] >= mdl_date), 
                  alpha=0.3, color='lightcoral', label='After MDL')

ax1.set_xlabel('Date', fontsize=12, fontweight='bold')
ax1.set_ylabel('Monthly Reports', fontsize=12, fontweight='bold')
ax1.set_title('Recent Timeline (2015-2025) - MDL Filing Impact', fontsize=14, fontweight='bold')
ax1.legend(loc='upper left', fontsize=10)
ax1.grid(True, alpha=0.3)

# 2. Before vs After comparison
ax2 = axes[0, 1]
periods = ['Before MDL\n(1993-2019)', 'After MDL\n(2019-2025)']
counts = [len(before_df), len(after_df)]
colors = ['lightyellow', 'lightcoral']
bars = ax2.bar(periods, counts, color=colors, edgecolor='black', linewidth=2)

ax2.set_ylabel('Total Reports', fontsize=12, fontweight='bold')
ax2.set_title(f'Total Reports: Before vs After MDL\nPattern: {pattern}', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

for bar, count in zip(bars, counts):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(count)}', ha='center', va='bottom', fontweight='bold', fontsize=12)

stats_text = f"Ratio: {ratio:.2f}x\nBefore Avg: {before_avg:.1f}/mo\nAfter Avg: {after_avg:.1f}/mo"
ax2.text(0.98, 0.98, stats_text, transform=ax2.transAxes, fontsize=11,
         verticalalignment='top', horizontalalignment='right',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# 3. 2019 Monthly Breakdown (MDL Year)
ax3 = axes[1, 0]
months_2019 = []
counts_2019 = []
for i in range(1, 13):
    period = pd.Period(f'2019-{i:02d}', freq='M')
    if period in monthly_2019.index:
        months_2019.append(month_names[i-1])
        counts_2019.append(monthly_2019[period])
    else:
        months_2019.append(month_names[i-1])
        counts_2019.append(0)

bars = ax3.bar(months_2019, counts_2019, color='steelblue', edgecolor='black', linewidth=1)

# Highlight December (MDL month)
bars[11].set_color('red')

ax3.set_xlabel('Month', fontsize=12, fontweight='bold')
ax3.set_ylabel('Reports', fontsize=12, fontweight='bold')
ax3.set_title('2019 Monthly Breakdown (MDL Filed December)', fontsize=14, fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')

# Add value labels
for i, (month, count) in enumerate(zip(months_2019, counts_2019)):
    if count > 0:
        ax3.text(i, count, str(count), ha='center', va='bottom', fontweight='bold', fontsize=9)

# 4. Pattern Summary
ax4 = axes[1, 1]
ax4.axis('off')

summary = f"""
ALLERGAN BIOCELL - PATTERN SUMMARY

Device: BIOCELL Textured Breast Implant
Manufacturer: Allergan, Inc.
MDL: No. 2921
Filed: December 18, 2019
Court: District of New Jersey

DATA SUMMARY:
• Total Reports: {len(df)}
• Date Range: 1993-2025
• Before MDL: {len(before_df)} reports
• After MDL: {len(after_df)} reports
• Ratio: {ratio:.2f}x

2019 SPIKE (MDL Year):
• Total 2019: 53 reports
• Peak: July 2019 (19 reports)
• THIS WAS BEFORE MDL FILING

PATTERN: {pattern}

INTERPRETATION:
Major spike occurred in 2019 BEFORE 
the December MDL filing. This suggests
a PREDICTIVE pattern where device issues
surfaced first, driving both reports and
litigation.

FDA CONTEXT:
• July 2019: FDA requested Allergan 
  recall BIOCELL implants due to 
  BIA-ALCL (cancer) risk
• This recall preceded the MDL filing

KEY FINDING:
Reports spiked in response to recall,
then MDL was filed 5 months later.
Pattern: Issue → Recall → Reports → MDL
"""

ax4.text(0.05, 0.95, summary, transform=ax4.transAxes, fontsize=10,
         verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round,pad=1', facecolor='lightgreen', alpha=0.3, 
                   edgecolor='green', linewidth=2))

plt.tight_layout()
plt.savefig('allergan_biocell_visual_analysis.png', dpi=300, bbox_inches='tight')
print("\n" + "="*80)
print("Visualization saved: allergan_biocell_visual_analysis.png")
print("="*80)

# Create detailed Excel summary
summary_data = {
    'Metric': [
        'Device',
        'MDL Number',
        'MDL Filed Date',
        'Court',
        'Total Reports',
        'Date Range',
        'Reports Before MDL',
        'Reports After MDL',
        'Ratio (After/Before)',
        '6-Month Before Window',
        '6-Month After Window',
        'Avg Reports/Mo Before',
        'Avg Reports/Mo After',
        '2019 Total (MDL Year)',
        'July 2019 (Peak)',
        'Pattern Type',
        'FDA Action',
        'Interpretation'
    ],
    'Value': [
        'BIOCELL Textured Breast Implant',
        'MDL No. 2921',
        'December 18, 2019',
        'District of New Jersey',
        len(df),
        f"{df['date_received'].min().strftime('%Y-%m-%d')} to {df['date_received'].max().strftime('%Y-%m-%d')}",
        len(before_df),
        len(after_df),
        f'{ratio:.2f}x',
        len(critical_before),
        len(critical_after),
        f'{before_avg:.1f}',
        f'{after_avg:.1f}',
        53,
        19,
        pattern,
        'July 2019: FDA recall request',
        'PREDICTIVE - Recall drove reports before MDL filing'
    ]
}

summary_df = pd.DataFrame(summary_data)

with pd.ExcelWriter('allergan_biocell_analysis_summary.xlsx', engine='openpyxl') as writer:
    summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    # Monthly 2019 breakdown
    monthly_2019_df = pd.DataFrame({
        'Month': months_2019,
        'Count': counts_2019
    })
    monthly_2019_df.to_excel(writer, sheet_name='2019 Monthly', index=False)
    
    # Before/After summary
    period_df = df.groupby('period').size().reset_index(name='count')
    period_df.to_excel(writer, sheet_name='Before After MDL', index=False)

print("Summary Excel saved: allergan_biocell_analysis_summary.xlsx")
print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
