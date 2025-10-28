import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (15, 10)

# Case filing dates
CASE_DATES = {
    'Bard PowerPort': '2022-08-01',
    'Cook Celect IVC Filter': '2014-08-01',
    'Bard G2 IVC Filter': '2015-04-01'
}

print("=" * 80)
print("CATHETER LITIGATION - MDR VISUALIZATION ANALYSIS")
print("Analyzing MDR patterns before and after litigation filing")
print("=" * 80)
print()

# Read the Excel file
file = 'catheter_devices_5years.xlsx'
df = pd.read_excel(file, sheet_name='All Devices Combined')

print(f"Total records loaded: {len(df):,}")
print()

# Parse dates
df['date_received'] = pd.to_datetime(df['date_received'])
df['year_month'] = df['date_received'].dt.to_period('M')

# Add case filing dates
df['case_filed'] = df['device_name'].map(CASE_DATES)
df['case_filed'] = pd.to_datetime(df['case_filed'])

# Calculate months before/after filing
df['months_from_filing'] = ((df['date_received'].dt.year - df['case_filed'].dt.year) * 12 + 
                             (df['date_received'].dt.month - df['case_filed'].dt.month))

# Create visualizations
fig, axes = plt.subplots(3, 2, figsize=(18, 15))
fig.suptitle('Catheter Litigation MDR Analysis: Before vs After Filing', fontsize=16, fontweight='bold')

devices = ['Bard PowerPort', 'Cook Celect IVC Filter', 'Bard G2 IVC Filter']

for idx, device in enumerate(devices):
    device_df = df[df['device_name'] == device].copy()
    case_date = pd.to_datetime(CASE_DATES[device])
    
    # Monthly counts
    monthly = device_df.groupby(device_df['date_received'].dt.to_period('M')).size()
    monthly.index = monthly.index.to_timestamp()
    
    # Plot 1: Full timeline with case filing marker (left column)
    ax1 = axes[idx, 0]
    ax1.plot(monthly.index, monthly.values, linewidth=2, marker='o', markersize=4, color='steelblue')
    ax1.axvline(x=case_date, color='red', linestyle='--', linewidth=2, label='Case Filed')
    ax1.set_title(f'{device}\nMonthly MDR Reports (2020-2025)', fontweight='bold')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Number of Reports')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Annotate case filing
    ymax = monthly.max()
    ax1.annotate('LITIGATION\nFILED', 
                xy=(case_date, ymax*0.8), 
                xytext=(case_date, ymax*0.9),
                ha='center',
                fontsize=10,
                fontweight='bold',
                color='red',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))
    
    # Plot 2: 12 months before/after comparison (right column)
    ax2 = axes[idx, 1]
    
    # Filter to 12 months before and after
    start_date = case_date - pd.DateOffset(months=12)
    end_date = case_date + pd.DateOffset(months=12)
    
    window_df = device_df[(device_df['date_received'] >= start_date) & 
                          (device_df['date_received'] <= end_date)].copy()
    
    window_monthly = window_df.groupby(window_df['date_received'].dt.to_period('M')).size()
    window_monthly.index = window_monthly.index.to_timestamp()
    
    # Color before/after differently
    before_mask = window_monthly.index < case_date
    after_mask = window_monthly.index >= case_date
    
    ax2.bar(window_monthly.index[before_mask], window_monthly.values[before_mask], 
            width=20, color='orange', alpha=0.7, label='Before Filing')
    ax2.bar(window_monthly.index[after_mask], window_monthly.values[after_mask], 
            width=20, color='green', alpha=0.7, label='After Filing')
    ax2.axvline(x=case_date, color='red', linestyle='--', linewidth=2, label='Case Filed')
    
    ax2.set_title(f'{device}\n12 Months Before/After Filing', fontweight='bold')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Number of Reports')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Calculate stats
    before_6mo = device_df[(device_df['date_received'] >= case_date - pd.DateOffset(months=6)) & 
                           (device_df['date_received'] < case_date)]
    after_6mo = device_df[(device_df['date_received'] >= case_date) & 
                          (device_df['date_received'] < case_date + pd.DateOffset(months=6))]
    
    print(f"\n{device}")
    print(f"  Case Filed: {case_date.strftime('%Y-%m-%d')}")
    print(f"  6 months before filing: {len(before_6mo):,} reports")
    print(f"  6 months after filing:  {len(after_6mo):,} reports")
    print(f"  Change: {(len(after_6mo) - len(before_6mo)) / len(before_6mo) * 100 if len(before_6mo) > 0 else 0:.1f}%")

plt.tight_layout()
plt.savefig('catheter_mdr_timeline_analysis.png', dpi=300, bbox_inches='tight')
print("\n✓ Saved: catheter_mdr_timeline_analysis.png")

# Create comparison chart
fig2, axes2 = plt.subplots(2, 2, figsize=(16, 12))
fig2.suptitle('Catheter Litigation MDR Patterns - Comparative Analysis', fontsize=16, fontweight='bold')

# Chart 1: Monthly trend comparison (all devices)
ax1 = axes2[0, 0]
for device in devices:
    device_df = df[df['device_name'] == device]
    monthly = device_df.groupby(device_df['date_received'].dt.to_period('M')).size()
    monthly.index = monthly.index.to_timestamp()
    ax1.plot(monthly.index, monthly.values, marker='o', label=device, linewidth=2)

ax1.set_title('Monthly MDR Trends - All Devices', fontweight='bold')
ax1.set_xlabel('Date')
ax1.set_ylabel('Number of Reports')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Chart 2: Event type distribution
ax2 = axes2[0, 1]
event_counts = df.groupby(['device_name', 'event_type']).size().unstack(fill_value=0)
event_counts.plot(kind='bar', ax=ax2, width=0.8)
ax2.set_title('Event Type Distribution by Device', fontweight='bold')
ax2.set_xlabel('Device')
ax2.set_ylabel('Number of Reports')
ax2.legend(title='Event Type', loc='upper right')
ax2.tick_params(axis='x', rotation=45)

# Chart 3: Before/After filing comparison
ax3 = axes2[1, 0]
comparison_data = []
for device in devices:
    device_df = df[df['device_name'] == device]
    case_date = pd.to_datetime(CASE_DATES[device])
    
    before = device_df[(device_df['date_received'] >= case_date - pd.DateOffset(months=12)) & 
                       (device_df['date_received'] < case_date)]
    after = device_df[(device_df['date_received'] >= case_date) & 
                      (device_df['date_received'] < case_date + pd.DateOffset(months=12))]
    
    comparison_data.append({
        'Device': device.replace(' IVC Filter', '').replace('Bard ', '').replace('Cook ', ''),
        '12 Mo Before': len(before),
        '12 Mo After': len(after)
    })

comp_df = pd.DataFrame(comparison_data)
comp_df.set_index('Device').plot(kind='bar', ax=ax3, width=0.7)
ax3.set_title('MDR Volume: 12 Months Before vs After Filing', fontweight='bold')
ax3.set_ylabel('Number of Reports')
ax3.legend(title='Period')
ax3.tick_params(axis='x', rotation=45)
ax3.grid(True, alpha=0.3, axis='y')

# Chart 4: Cumulative reports over time
ax4 = axes2[1, 1]
for device in devices:
    device_df = df[df['device_name'] == device].sort_values('date_received')
    device_df['cumulative'] = range(1, len(device_df) + 1)
    case_date = pd.to_datetime(CASE_DATES[device])
    
    ax4.plot(device_df['date_received'], device_df['cumulative'], 
            label=device, linewidth=2, marker='o', markersize=3)
    
    # Mark case filing point
    filing_point = device_df[device_df['date_received'] >= case_date].iloc[0]
    ax4.scatter(filing_point['date_received'], filing_point['cumulative'], 
               s=200, marker='*', edgecolors='red', linewidths=2, zorder=5)

ax4.set_title('Cumulative MDR Reports (Stars = Litigation Filed)', fontweight='bold')
ax4.set_xlabel('Date')
ax4.set_ylabel('Cumulative Reports')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('catheter_mdr_comparison_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: catheter_mdr_comparison_analysis.png")

# Create detailed statistical summary
print("\n" + "=" * 80)
print("STATISTICAL SUMMARY")
print("=" * 80)

summary_data = []
for device in devices:
    device_df = df[df['device_name'] == device]
    case_date = pd.to_datetime(CASE_DATES[device])
    
    # Different time windows
    periods = [
        ('6 Mo Before', -6, 0),
        ('3 Mo Before', -3, 0),
        ('1 Mo Before', -1, 0),
        ('1 Mo After', 0, 1),
        ('3 Mo After', 0, 3),
        ('6 Mo After', 0, 6),
        ('12 Mo After', 0, 12)
    ]
    
    for label, start_months, end_months in periods:
        start = case_date + pd.DateOffset(months=start_months)
        end = case_date + pd.DateOffset(months=end_months)
        
        period_df = device_df[(device_df['date_received'] >= start) & 
                              (device_df['date_received'] < end)]
        
        summary_data.append({
            'Device': device,
            'Period': label,
            'Reports': len(period_df),
            'Avg per Month': len(period_df) / abs(start_months - end_months) if start_months != end_months else len(period_df)
        })

summary_df = pd.DataFrame(summary_data)

print("\nREPORTS BY PERIOD:")
for device in devices:
    print(f"\n{device}:")
    device_summary = summary_df[summary_df['Device'] == device]
    print(device_summary[['Period', 'Reports', 'Avg per Month']].to_string(index=False))

# Save summary to Excel
with pd.ExcelWriter('catheter_mdr_analysis_summary.xlsx', engine='openpyxl') as writer:
    summary_df.to_excel(writer, sheet_name='Time Period Summary', index=False)
    
    # Add monthly breakdown
    for device in devices:
        device_df = df[df['device_name'] == device]
        monthly = device_df.groupby(device_df['date_received'].dt.to_period('M')).size().reset_index()
        monthly.columns = ['Month', 'Report Count']
        sheet_name = device[:31]
        monthly.to_excel(writer, sheet_name=sheet_name, index=False)

print("\n✓ Saved: catheter_mdr_analysis_summary.xlsx")

print("\n" + "=" * 80)
print("COMPLETE - 3 FILES CREATED:")
print("=" * 80)
print("1. catheter_mdr_timeline_analysis.png - Individual device timelines")
print("2. catheter_mdr_comparison_analysis.png - Comparative charts")
print("3. catheter_mdr_analysis_summary.xlsx - Statistical summary")
print("=" * 80)
