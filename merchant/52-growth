# M5B-1: GROWTH LEADERS & DECLINERS - ANALYSIS
# Identifies merchants with biggest month-over-month spend changes
print("\n" + "="*120)
print(" " * 40 + "M5B-1: GROWTH LEADERS & DECLINERS - ANALYSIS")
print("="*120)

# Calculate month-over-month changes for each merchant
sorted_months = sorted(combined_df['year_month'].unique())

growth_data = []

for i in range(1, len(sorted_months)):
    prev_month = sorted_months[i-1]
    curr_month = sorted_months[i]
    
    # Previous month spending
    prev_spend = combined_df[combined_df['year_month'] == prev_month].groupby('merchant_consolidated')['amount'].sum()
    
    # Current month spending
    curr_spend = combined_df[combined_df['year_month'] == curr_month].groupby('merchant_consolidated')['amount'].sum()
    
    # Calculate changes for merchants in both months
    for merchant in set(prev_spend.index) & set(curr_spend.index):
        prev_amt = prev_spend[merchant]
        curr_amt = curr_spend[merchant]
        change_amt = curr_amt - prev_amt
        change_pct = (change_amt / prev_amt * 100) if prev_amt > 0 else 0
        
        # Only include significant merchants (min $1000 in either month)
        if max(prev_amt, curr_amt) >= 1000:
            growth_data.append({
                'merchant': merchant,
                'month_pair': f"{prev_month} → {curr_month}",
                'prev_month': prev_month,
                'curr_month': curr_month,
                'prev_spend': prev_amt,
                'curr_spend': curr_amt,
                'change_amount': change_amt,
                'change_percent': change_pct
            })

growth_df = pd.DataFrame(growth_data)

# TOP GROWTH LEADERS
print("\n📈 TOP 50 GROWTH LEADERS (Largest $ Increases)")
print("="*120)

top_growth = growth_df.nlargest(50, 'change_amount').copy()
top_growth['merchant'] = top_growth['merchant'].str[:40]
top_growth_display = top_growth[[
    'merchant', 'month_pair', 'prev_spend', 'curr_spend', 'change_amount', 'change_percent'
]].copy()

top_growth_display.columns = ['Merchant', 'Period', 'Previous Month', 'Current Month', 'Change ($)', 'Change (%)']

# Format currency and percentages
top_growth_display['Previous Month'] = top_growth_display['Previous Month'].apply(lambda x: f"${x:,.0f}")
top_growth_display['Current Month'] = top_growth_display['Current Month'].apply(lambda x: f"${x:,.0f}")
top_growth_display['Change ($)'] = top_growth_display['Change ($)'].apply(lambda x: f"${x:,.0f}")
top_growth_display['Change (%)'] = top_growth_display['Change (%)'].apply(lambda x: f"{x:,.1f}%")

display(top_growth_display.style.hide(axis='index'))

print("\n" + "="*120)

# TOP DECLINERS
print("\n📉 TOP 50 DECLINERS (Largest $ Decreases)")
print("="*120)

top_decline = growth_df.nsmallest(50, 'change_amount').copy()
top_decline['merchant'] = top_decline['merchant'].str[:40]
top_decline_display = top_decline[[
    'merchant', 'month_pair', 'prev_spend', 'curr_spend', 'change_amount', 'change_percent'
]].copy()

top_decline_display.columns = ['Merchant', 'Period', 'Previous Month', 'Current Month', 'Change ($)', 'Change (%)']

# Format currency and percentages
top_decline_display['Previous Month'] = top_decline_display['Previous Month'].apply(lambda x: f"${x:,.0f}")
top_decline_display['Current Month'] = top_decline_display['Current Month'].apply(lambda x: f"${x:,.0f}")
top_decline_display['Change ($)'] = top_decline_display['Change ($)'].apply(lambda x: f"${x:,.0f}")
top_decline_display['Change (%)'] = top_decline_display['Change (%)'].apply(lambda x: f"{x:,.1f}%")

display(top_decline_display.style.hide(axis='index'))

print("\n💡 SUMMARY STATISTICS:")
print("-"*120)
print(f"   • Total month-over-month comparisons analyzed: {len(growth_df):,}")
print(f"   • Average absolute change: ${growth_df['change_amount'].abs().mean():,.0f}")
print(f"   • Median change: ${growth_df['change_amount'].median():,.0f}")
print(f"   • Merchants with increases: {(growth_df['change_amount'] > 0).sum():,} ({(growth_df['change_amount'] > 0).sum() / len(growth_df) * 100:.1f}%)")
print(f"   • Merchants with decreases: {(growth_df['change_amount'] < 0).sum():,} ({(growth_df['change_amount'] < 0).sum() / len(growth_df) * 100:.1f}%)")
print("="*120)
