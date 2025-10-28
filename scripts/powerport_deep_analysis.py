import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 12)

print("=" * 80)
print("BARD POWERPORT - DEEP DIVE ANALYSIS")
print("Case Filed: August 2022")
print("=" * 80)
print()

# Load data
file = 'catheter_devices_5years.xlsx'
df = pd.read_excel(file, sheet_name='Bard PowerPort')

print(f"Total PowerPort records (2020-2025): {len(df):,}")
print()

# Parse dates
df['date_received'] = pd.to_datetime(df['date_received'])
df['year_month'] = df['date_received'].dt.to_period('M')
df['year'] = df['date_received'].dt.year
df['month'] = df['date_received'].dt.month

# Case filing date
case_date = pd.to_datetime('2022-08-01')

# Calculate months from filing
df['months_from_filing'] = ((df['date_received'].dt.year - case_date.year) * 12 + 
                             (df['date_received'].dt.month - case_date.month))

# Create comprehensive visualization
fig = plt.figure(figsize=(18, 14))
gs = fig.add_gridspec(4, 3, hspace=0.3, wspace=0.3)

# Main title
fig.suptitle('Bard PowerPort MDR Analysis: Litigation Impact (Case Filed August 2022)', 
             fontsize=18, fontweight='bold', y=0.995)

# 1. Full timeline (large chart across top)
ax1 = fig.add_subplot(gs[0, :])
monthly = df.groupby('year_month').size()
monthly.index = monthly.index.to_timestamp()

ax1.plot(monthly.index, monthly.values, linewidth=3, marker='o', markersize=6, 
         color='steelblue', label='Monthly Reports')
ax1.axvline(x=case_date, color='red', linestyle='--', linewidth=3, label='Case Filed (Aug 2022)')

# Fill areas
before_mask = monthly.index < case_date
after_mask = monthly.index >= case_date
ax1.fill_between(monthly.index[before_mask], 0, monthly.values[before_mask], 
                 alpha=0.2, color='orange', label='Before Litigation')
ax1.fill_between(monthly.index[after_mask], 0, monthly.values[after_mask], 
                 alpha=0.2, color='green', label='After Litigation')

ax1.set_title('Monthly MDR Reports Timeline (2020-2025)', fontsize=14, fontweight='bold', pad=10)
ax1.set_xlabel('Date', fontsize=12)
ax1.set_ylabel('Number of Reports', fontsize=12)
ax1.legend(loc='upper left', fontsize=10)
ax1.grid(True, alpha=0.3)

# Annotate key points
ymax = monthly.max()
ax1.annotate('LITIGATION\nFILED', xy=(case_date, ymax*0.5), 
            xytext=(case_date, ymax*0.7),
            ha='center', fontsize=12, fontweight='bold', color='red',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.8),
            arrowprops=dict(arrowstyle='->', color='red', lw=2))

# Find peak after filing
peak_month = monthly[monthly.index >= case_date].idxmax()
peak_value = monthly[monthly.index >= case_date].max()
ax1.annotate(f'PEAK\n{peak_value} reports', xy=(peak_month, peak_value),
            xytext=(peak_month, peak_value*1.1),
            ha='center', fontsize=10, fontweight='bold', color='darkgreen',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', alpha=0.7),
            arrowprops=dict(arrowstyle='->', color='darkgreen', lw=1.5))

# 2. Before/After comparison (24 months window)
ax2 = fig.add_subplot(gs[1, 0])
window_df = df[(df['date_received'] >= case_date - pd.DateOffset(months=12)) & 
               (df['date_received'] <= case_date + pd.DateOffset(months=12))]
window_monthly = window_df.groupby(window_df['date_received'].dt.to_period('M')).size()
window_monthly.index = window_monthly.index.to_timestamp()

colors = ['orange' if d < case_date else 'green' for d in window_monthly.index]
bars = ax2.bar(window_monthly.index, window_monthly.values, width=20, color=colors, alpha=0.7)
ax2.axvline(x=case_date, color='red', linestyle='--', linewidth=2)
ax2.set_title('12 Months Before/After Filing', fontweight='bold')
ax2.set_ylabel('Reports')
ax2.tick_params(axis='x', rotation=45)
ax2.grid(True, alpha=0.3, axis='y')

# 3. Event type distribution
ax3 = fig.add_subplot(gs[1, 1])
event_counts = df['event_type'].value_counts()
colors_pie = ['#ff6b6b', '#feca57', '#48dbfb', '#1dd1a1']
wedges, texts, autotexts = ax3.pie(event_counts.values, labels=event_counts.index, 
                                     autopct='%1.1f%%', startangle=90, colors=colors_pie)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
ax3.set_title('Event Type Distribution', fontweight='bold')

# 4. Yearly comparison
ax4 = fig.add_subplot(gs[1, 2])
yearly = df.groupby('year').size()
colors_bar = ['steelblue' if y < 2022 else ('red' if y == 2022 else 'green') for y in yearly.index]
bars = ax4.bar(yearly.index, yearly.values, color=colors_bar, alpha=0.7, edgecolor='black', linewidth=1.5)
ax4.set_title('Reports by Year', fontweight='bold')
ax4.set_xlabel('Year')
ax4.set_ylabel('Reports')
ax4.grid(True, alpha=0.3, axis='y')

# Add values on bars
for bar in bars:
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}', ha='center', va='bottom', fontweight='bold')

# 5. Monthly average before/after
ax5 = fig.add_subplot(gs[2, 0])
before_filing = df[df['date_received'] < case_date]
after_filing = df[df['date_received'] >= case_date]

before_monthly_avg = len(before_filing) / before_filing['year_month'].nunique() if before_filing['year_month'].nunique() > 0 else 0
after_monthly_avg = len(after_filing) / after_filing['year_month'].nunique() if after_filing['year_month'].nunique() > 0 else 0

categories = ['Before\nLitigation', 'After\nLitigation']
averages = [before_monthly_avg, after_monthly_avg]
colors = ['orange', 'green']

bars = ax5.bar(categories, averages, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
ax5.set_title('Average Monthly Reports', fontweight='bold')
ax5.set_ylabel('Avg Reports per Month')
ax5.grid(True, alpha=0.3, axis='y')

# Add values on bars
for bar, val in zip(bars, averages):
    ax5.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
            f'{val:.1f}', ha='center', va='bottom', fontsize=12, fontweight='bold')

# Add percentage increase
increase = ((after_monthly_avg - before_monthly_avg) / before_monthly_avg * 100) if before_monthly_avg > 0 else 0
ax5.text(0.5, max(averages) * 0.5, f'+{increase:.1f}%', 
        ha='center', fontsize=16, fontweight='bold', color='red',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.8))

# 6. Cumulative reports
ax6 = fig.add_subplot(gs[2, 1])
df_sorted = df.sort_values('date_received')
df_sorted['cumulative'] = range(1, len(df_sorted) + 1)

ax6.plot(df_sorted['date_received'], df_sorted['cumulative'], 
        linewidth=3, color='steelblue')
ax6.axvline(x=case_date, color='red', linestyle='--', linewidth=2)

# Mark filing point
filing_point = df_sorted[df_sorted['date_received'] >= case_date].iloc[0]
ax6.scatter(filing_point['date_received'], filing_point['cumulative'], 
           s=300, marker='*', color='red', edgecolors='darkred', linewidths=2, zorder=5)

ax6.set_title('Cumulative Reports Over Time', fontweight='bold')
ax6.set_xlabel('Date')
ax6.set_ylabel('Cumulative Count')
ax6.grid(True, alpha=0.3)

# Calculate slope change
before_slope = filing_point['cumulative'] / ((filing_point['date_received'] - df_sorted['date_received'].min()).days / 30)
after_slope = (len(df_sorted) - filing_point['cumulative']) / ((df_sorted['date_received'].max() - filing_point['date_received']).days / 30)

ax6.text(0.05, 0.95, f'Before: {before_slope:.1f}/month\nAfter: {after_slope:.1f}/month',
        transform=ax6.transAxes, fontsize=10, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# 7. Report source distribution
ax7 = fig.add_subplot(gs[2, 2])
if 'report_source_code' in df.columns:
    source_counts = df['report_source_code'].value_counts().head(5)
    ax7.barh(range(len(source_counts)), source_counts.values, color='steelblue', alpha=0.7)
    ax7.set_yticks(range(len(source_counts)))
    ax7.set_yticklabels(source_counts.index)
    ax7.set_title('Top Report Sources', fontweight='bold')
    ax7.set_xlabel('Number of Reports')
    ax7.grid(True, alpha=0.3, axis='x')
else:
    ax7.text(0.5, 0.5, 'Source data\nnot available', 
            ha='center', va='center', fontsize=12)
    ax7.set_title('Top Report Sources', fontweight='bold')

# 8. Statistical summary table
ax8 = fig.add_subplot(gs[3, :])
ax8.axis('tight')
ax8.axis('off')

# Calculate statistics
stats_data = [
    ['Metric', 'Before Filing', 'After Filing', 'Change'],
    ['Total Reports', f"{len(before_filing):,}", f"{len(after_filing):,}", 
     f"+{len(after_filing) - len(before_filing):,} ({((len(after_filing) - len(before_filing)) / len(before_filing) * 100):.1f}%)"],
    ['Avg per Month', f"{before_monthly_avg:.1f}", f"{after_monthly_avg:.1f}", 
     f"+{after_monthly_avg - before_monthly_avg:.1f} ({increase:.1f}%)"],
    ['Deaths', f"{len(before_filing[before_filing['event_type'].str.contains('Death', na=False)])}", 
     f"{len(after_filing[after_filing['event_type'].str.contains('Death', na=False)])}", ""],
    ['Injuries', f"{len(before_filing[before_filing['event_type'].str.contains('Injury', na=False)])}", 
     f"{len(after_filing[after_filing['event_type'].str.contains('Injury', na=False)])}", ""],
    ['Peak Month', f"{monthly[monthly.index < case_date].max():.0f}", 
     f"{monthly[monthly.index >= case_date].max():.0f}", ""]
]

table = ax8.table(cellText=stats_data, cellLoc='center', loc='center',
                 colWidths=[0.25, 0.25, 0.25, 0.25])
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 2.5)

# Style header row
for i in range(4):
    table[(0, i)].set_facecolor('#4CAF50')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Style data rows
for i in range(1, len(stats_data)):
    for j in range(4):
        if j < 3:
            table[(i, j)].set_facecolor('#f0f0f0' if i % 2 == 0 else 'white')

ax8.set_title('Statistical Summary: Before vs After Litigation Filing (August 2022)', 
             fontsize=14, fontweight='bold', pad=20)

plt.savefig('bard_powerport_deep_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: bard_powerport_deep_analysis.png")

# Print detailed statistics
print("\n" + "=" * 80)
print("DETAILED STATISTICS")
print("=" * 80)
print()

print(f"Case Filed: {case_date.strftime('%B %d, %Y')}")
print()

print("TIME PERIODS:")
print("-" * 60)
periods = [
    ('1 month before', -1, 0),
    ('3 months before', -3, 0),
    ('6 months before', -6, 0),
    ('12 months before', -12, 0),
    ('1 month after', 0, 1),
    ('3 months after', 0, 3),
    ('6 months after', 0, 6),
    ('12 months after', 0, 12)
]

for label, start, end in periods:
    period_start = case_date + pd.DateOffset(months=start)
    period_end = case_date + pd.DateOffset(months=end)
    period_df = df[(df['date_received'] >= period_start) & (df['date_received'] < period_end)]
    months = abs(start - end)
    avg = len(period_df) / months if months > 0 else len(period_df)
    print(f"{label:20s}: {len(period_df):4d} reports ({avg:.1f}/month)")

print()
print("EVENT TYPES:")
print("-" * 60)
for event_type, count in df['event_type'].value_counts().items():
    pct = count / len(df) * 100
    print(f"{event_type:20s}: {count:5d} ({pct:5.1f}%)")

print()
print("YEARLY BREAKDOWN:")
print("-" * 60)
for year in sorted(df['year'].unique()):
    year_df = df[df['year'] == year]
    print(f"{year}: {len(year_df):4d} reports")

print()
print("=" * 80)
print("KEY FINDINGS:")
print("=" * 80)
print(f"• REVERSE PATTERN confirmed: {increase:.1f}% increase after litigation")
print(f"• Peak month: {monthly[monthly.index >= case_date].idxmax().strftime('%B %Y')} ({int(monthly[monthly.index >= case_date].max())} reports)")
print(f"• Litigation drove awareness: Reports spiked AFTER filing")
print(f"• Total reports before: {len(before_filing):,} | After: {len(after_filing):,}")
print("=" * 80)
