# M5B-3: DECLINERS VISUALIZATION
print("\n" + "="*120)
print("📉 DECLINERS - VISUALIZATION")
print("="*120)

# Rebuild growth_df (in case cells run separately)
sorted_months = sorted(combined_df['year_month'].unique())
growth_data = []

for i in range(1, len(sorted_months)):
    prev_month = sorted_months[i-1]
    curr_month = sorted_months[i]
    prev_spend = combined_df[combined_df['year_month'] == prev_month].groupby('merchant_consolidated')['amount'].sum()
    curr_spend = combined_df[combined_df['year_month'] == curr_month].groupby('merchant_consolidated')['amount'].sum()
    
    for merchant in set(prev_spend.index) & set(curr_spend.index):
        prev_amt = prev_spend[merchant]
        curr_amt = curr_spend[merchant]
        change_amt = curr_amt - prev_amt
        change_pct = (change_amt / prev_amt * 100) if prev_amt > 0 else 0
        
        if max(prev_amt, curr_amt) >= 1000:
            growth_data.append({
                'merchant': merchant,
                'change_amount': change_amt,
                'change_percent': change_pct
            })

growth_df = pd.DataFrame(growth_data)

# Create visualization
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 10))

plot_data = growth_df.nsmallest(50, 'change_amount').copy()
plot_data = plot_data.sort_values('change_amount', ascending=False)  # Most negative at top

merchants = plot_data['merchant'].str[:35]
changes = plot_data['change_amount']

bars = ax.barh(range(len(merchants)), changes, color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=0.5)

ax.set_yticks(range(len(merchants)))
ax.set_yticklabels([f"#{i+1} {m}" for i, m in enumerate(merchants)], fontsize=8)
ax.set_xlabel('Month-over-Month Spend Decrease ($)', fontsize=11, fontweight='bold')
ax.set_title('Top 50 Decliners - Largest Spend Decreases', fontsize=13, fontweight='bold', pad=15)

# Add value labels
for i, (bar, val) in enumerate(zip(bars, changes)):
    ax.text(val, bar.get_y() + bar.get_height()/2, f' ${val:,.0f}', 
            va='center', fontsize=7, fontweight='bold')

ax.grid(axis='x', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.show()

print("="*120)
