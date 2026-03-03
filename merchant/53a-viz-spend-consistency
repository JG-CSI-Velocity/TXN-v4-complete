# M5C-2: CONSISTENT MERCHANTS VISUALIZATION
print("\n" + "="*120)
print("📊 MOST CONSISTENT MERCHANTS - VISUALIZATION")
print("="*120)

# Rebuild consistency_df (in case cells run separately)
sorted_months = sorted(combined_df['year_month'].unique())
merchant_monthly = combined_df.groupby(['merchant_consolidated', 'year_month'])['amount'].sum().reset_index()
spending_pivot = merchant_monthly.pivot(index='merchant_consolidated', columns='year_month', values='amount').fillna(0)

consistency_data = []
for merchant in spending_pivot.index:
    monthly_values = spending_pivot.loc[merchant].values
    non_zero_values = monthly_values[monthly_values > 0]
    
    if len(non_zero_values) >= 3:
        total_spend = non_zero_values.sum()
        mean_spend = non_zero_values.mean()
        std_spend = non_zero_values.std()
        cv = (std_spend / mean_spend * 100) if mean_spend > 0 else 0
        months_active = len(non_zero_values)
        
        consistency_data.append({
            'merchant': merchant,
            'coefficient_variation': cv,
            'consistency_score': 100 - min(cv, 100)
        })

consistency_df = pd.DataFrame(consistency_data)

# Visualization
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 10))

plot_data = consistency_df.nlargest(50, 'consistency_score').head(50).sort_values('coefficient_variation', ascending=False)

merchants = plot_data['merchant'].str[:35]
cv_values = plot_data['coefficient_variation']

bars = ax.barh(range(len(merchants)), cv_values, color='#3498db', alpha=0.8, edgecolor='black', linewidth=0.5)

ax.set_yticks(range(len(merchants)))
ax.set_yticklabels([f"#{i+1} {m}" for i, m in enumerate(merchants)], fontsize=8)
ax.set_xlabel('Coefficient of Variation (%)', fontsize=11, fontweight='bold')
ax.set_title('Top 50 Most Consistent Merchants - Lowest Spending Variation', fontsize=13, fontweight='bold', pad=15)

# Add value labels
for i, (bar, val) in enumerate(zip(bars, cv_values)):
    ax.text(val, bar.get_y() + bar.get_height()/2, f' {val:.1f}%', 
            va='center', fontsize=7, fontweight='bold')

ax.grid(axis='x', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.show()

print("="*120)
