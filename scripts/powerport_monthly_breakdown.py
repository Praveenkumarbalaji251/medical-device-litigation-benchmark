import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("=" * 80)
print("BARD POWERPORT - MONTHLY BREAKDOWN ANALYSIS")
print("Detailed month-by-month report counts")
print("=" * 80)
print()

# Load data
file = 'catheter_devices_5years.xlsx'
df = pd.read_excel(file, sheet_name='Bard PowerPort')

# Parse dates
df['date_received'] = pd.to_datetime(df['date_received'])

# Get monthly breakdown
monthly = df.groupby(df['date_received'].dt.to_period('M')).agg({
    'report_number': 'count',
    'event_type': lambda x: ', '.join(x.value_counts().head(2).index.tolist())
}).reset_index()
monthly.columns = ['Month', 'Report Count', 'Top Event Types']
monthly['Month'] = monthly['Month'].dt.to_timestamp()

# Add year-month string for display
monthly['YearMonth'] = monthly['Month'].dt.strftime('%Y-%m')

# Case filing date
case_date = pd.to_datetime('2022-08-01')
monthly['Period'] = monthly['Month'].apply(lambda x: 'BEFORE' if x < case_date else 'AFTER')

print("COMPLETE MONTHLY BREAKDOWN (2020-2025)")
print("=" * 80)
print()

# Print all months
print(f"{'Month':12s} {'Reports':>8s}  {'Period':8s}  {'Top Event Types'}")
print("-" * 80)

for idx, row in monthly.iterrows():
    month_str = row['Month'].strftime('%Y-%m')
    reports = row['Report Count']
    period = row['Period']
    events = row['Top Event Types'][:50]  # Truncate if too long
    
    # Highlight litigation month
    if row['Month'].year == 2022 and row['Month'].month == 8:
        print(f"{month_str:12s} {reports:8d}  >>> LITIGATION FILED <<<")
    else:
        print(f"{month_str:12s} {reports:8d}  {period:8s}  {events}")

# Calculate statistics by period
print()
print("=" * 80)
print("SUMMARY STATISTICS")
print("=" * 80)
print()

before = monthly[monthly['Period'] == 'BEFORE']
after = monthly[monthly['Period'] == 'AFTER']

print("BEFORE LITIGATION (Jan 2020 - July 2022):")
print("-" * 60)
print(f"  Total months: {len(before)}")
print(f"  Total reports: {before['Report Count'].sum():,}")
print(f"  Average per month: {before['Report Count'].mean():.1f}")
print(f"  Median per month: {before['Report Count'].median():.1f}")
print(f"  Min: {before['Report Count'].min()} | Max: {before['Report Count'].max()}")
print(f"  Std Dev: {before['Report Count'].std():.1f}")
print()

print("AFTER LITIGATION (Aug 2022 - Sep 2025):")
print("-" * 60)
print(f"  Total months: {len(after)}")
print(f"  Total reports: {after['Report Count'].sum():,}")
print(f"  Average per month: {after['Report Count'].mean():.1f}")
print(f"  Median per month: {after['Report Count'].median():.1f}")
print(f"  Min: {after['Report Count'].min()} | Max: {after['Report Count'].max()}")
print(f"  Std Dev: {after['Report Count'].std():.1f}")
print()

# Find top months
print("TOP 10 HIGHEST MONTHS:")
print("-" * 60)
top_months = monthly.nlargest(10, 'Report Count')
for idx, row in top_months.iterrows():
    month_str = row['Month'].strftime('%Y-%m')
    reports = row['Report Count']
    period = row['Period']
    print(f"  {month_str}: {reports:4d} reports ({period})")

print()

# Find lowest months
print("BOTTOM 10 LOWEST MONTHS:")
print("-" * 60)
bottom_months = monthly.nsmallest(10, 'Report Count')
for idx, row in bottom_months.iterrows():
    month_str = row['Month'].strftime('%Y-%m')
    reports = row['Report Count']
    period = row['Period']
    print(f"  {month_str}: {reports:4d} reports ({period})")

print()

# Year-over-year comparison
print("=" * 80)
print("YEAR-OVER-YEAR MONTHLY COMPARISON")
print("=" * 80)
print()

# Create pivot table
monthly['Year'] = monthly['Month'].dt.year
monthly['MonthNum'] = monthly['Month'].dt.month

pivot = monthly.pivot(index='MonthNum', columns='Year', values='Report Count').fillna(0)

# Month names
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

print(f"{'Month':8s}", end='')
for year in sorted(pivot.columns):
    print(f"{year:>8d}", end='')
print()
print("-" * (8 + 8 * len(pivot.columns)))

for month_num in range(1, 13):
    if month_num in pivot.index:
        print(f"{month_names[month_num-1]:8s}", end='')
        for year in sorted(pivot.columns):
            val = pivot.loc[month_num, year]
            print(f"{int(val):8d}", end='')
        print()

# Save to Excel
output_file = 'powerport_monthly_breakdown.xlsx'

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # All months
    monthly_export = monthly[['YearMonth', 'Report Count', 'Period', 'Top Event Types']].copy()
    monthly_export.columns = ['Month', 'Reports', 'Period', 'Top Event Types']
    monthly_export.to_excel(writer, sheet_name='Monthly Breakdown', index=False)
    
    # Pivot table
    pivot.to_excel(writer, sheet_name='Year Over Year')
    
    # Summary stats
    summary_data = pd.DataFrame([
        ['Before Litigation', len(before), before['Report Count'].sum(), 
         before['Report Count'].mean(), before['Report Count'].median(),
         before['Report Count'].min(), before['Report Count'].max()],
        ['After Litigation', len(after), after['Report Count'].sum(),
         after['Report Count'].mean(), after['Report Count'].median(),
         after['Report Count'].min(), after['Report Count'].max()]
    ], columns=['Period', 'Months', 'Total Reports', 'Avg/Month', 'Median/Month', 'Min', 'Max'])
    summary_data.to_excel(writer, sheet_name='Summary Stats', index=False)
    
    # Top/Bottom months
    top_months_export = top_months[['YearMonth', 'Report Count', 'Period']].copy()
    top_months_export.columns = ['Month', 'Reports', 'Period']
    top_months_export.to_excel(writer, sheet_name='Top 10 Months', index=False)
    
    bottom_months_export = bottom_months[['YearMonth', 'Report Count', 'Period']].copy()
    bottom_months_export.columns = ['Month', 'Reports', 'Period']
    bottom_months_export.to_excel(writer, sheet_name='Bottom 10 Months', index=False)

print()
print("=" * 80)
print(f"✓ Detailed breakdown saved to: {output_file}")
print("=" * 80)
print()

print("SHEETS INCLUDED:")
print("  1. Monthly Breakdown - All months with counts")
print("  2. Year Over Year - Pivot table comparison")
print("  3. Summary Stats - Before/After statistics")
print("  4. Top 10 Months - Highest reporting months")
print("  5. Bottom 10 Months - Lowest reporting months")
print()

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Bard PowerPort - Monthly Breakdown Analysis', fontsize=16, fontweight='bold')

# 1. All months bar chart
ax1 = axes[0, 0]
colors = ['orange' if p == 'BEFORE' else 'green' for p in monthly['Period']]
ax1.bar(range(len(monthly)), monthly['Report Count'], color=colors, alpha=0.7)
ax1.axvline(x=len(before)-0.5, color='red', linestyle='--', linewidth=3, label='Litigation Filed')
ax1.set_title('Monthly Reports: All Months (2020-2025)', fontweight='bold')
ax1.set_xlabel('Months (chronological)')
ax1.set_ylabel('Number of Reports')
ax1.legend()
ax1.grid(True, alpha=0.3, axis='y')

# 2. Box plot before/after
ax2 = axes[0, 1]
data_to_plot = [before['Report Count'], after['Report Count']]
bp = ax2.boxplot(data_to_plot, labels=['Before\nLitigation', 'After\nLitigation'],
                 patch_artist=True, widths=0.6)
bp['boxes'][0].set_facecolor('orange')
bp['boxes'][1].set_facecolor('green')
for patch in bp['boxes']:
    patch.set_alpha(0.7)
ax2.set_title('Distribution Comparison', fontweight='bold')
ax2.set_ylabel('Reports per Month')
ax2.grid(True, alpha=0.3, axis='y')

# Add mean markers
means = [before['Report Count'].mean(), after['Report Count'].mean()]
ax2.scatter([1, 2], means, color='red', s=100, zorder=5, label='Mean')
ax2.legend()

# 3. Year-over-year heatmap
ax3 = axes[1, 0]
pivot_display = pivot.loc[:, pivot.columns >= 2020]  # Only 2020+
sns.heatmap(pivot_display, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax3, cbar_kws={'label': 'Reports'})
ax3.set_title('Year-Over-Year Monthly Heatmap', fontweight='bold')
ax3.set_xlabel('Year')
ax3.set_ylabel('Month')
ax3.set_yticklabels(month_names, rotation=0)

# 4. Cumulative by period
ax4 = axes[1, 1]
monthly_sorted = monthly.sort_values('Month')
before_cum = before.sort_values('Month')['Report Count'].cumsum()
after_cum = after.sort_values('Month')['Report Count'].cumsum()

ax4.plot(range(len(before_cum)), before_cum.values, 
        linewidth=3, marker='o', color='orange', label='Before Litigation')
ax4.plot(range(len(before_cum), len(before_cum) + len(after_cum)), 
        after_cum.values + before_cum.iloc[-1], 
        linewidth=3, marker='o', color='green', label='After Litigation')
ax4.axvline(x=len(before_cum)-0.5, color='red', linestyle='--', linewidth=2)
ax4.set_title('Cumulative Reports by Period', fontweight='bold')
ax4.set_xlabel('Months')
ax4.set_ylabel('Cumulative Reports')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('powerport_monthly_breakdown_charts.png', dpi=300, bbox_inches='tight')
print("✓ Visualization saved to: powerport_monthly_breakdown_charts.png")
print()
