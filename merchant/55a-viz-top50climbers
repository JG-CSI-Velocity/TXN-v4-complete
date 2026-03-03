# M5F-2: PERSONAL RANK CLIMBERS VISUALIZATION
print("\n" + "="*120)
print("📈 PERSONAL RANK CLIMBERS - VISUALIZATION")
print("="*120)

import matplotlib.pyplot as plt

# Rebuild movers_df
sorted_months = sorted(personal_df['year_month'].unique())
monthly_movers = []

for i in range(1, len(sorted_months)):
    prev_month = sorted_months[i-1]
    curr_month = sorted_months[i]
    prev_data = personal_df[personal_df['year_month'] == prev_month]
    prev_rankings = prev_data.groupby('merchant_consolidated')['amount'].sum().sort_values(ascending=False)
    prev_rankings = prev_rankings.reset_index()
    prev_rankings['rank'] = range(1, len(prev_rankings) + 1)
    prev_rankings = prev_rankings.set_index('merchant_consolidated')
    
    curr_data = personal_df[personal_df['year_month'] == curr_month]
    curr_rankings = curr_data.groupby('merchant_consolidated')['amount'].sum().sort_values(ascending=False)
    curr_rankings = curr_rankings.reset_index()
    curr_rankings['rank'] = range(1, len(curr_rankings) + 1)
    curr_rankings = curr_rankings.set_index('merchant_consolidated')
    
    common = set(prev_rankings.index) & set(curr_rankings.index)
    
    for merchant in common:
        prev_rank = prev_rankings.loc[merchant, 'rank']
        curr_rank = curr_rankings.loc[merchant, 'rank']
        rank_change = prev_rank - curr_rank
        
        if prev_rank <= 100 or curr_rank <= 100:
            monthly_movers.append({'merchant': merchant, 'rank_change': rank_change})

movers_df = pd.DataFrame(monthly_movers)
top_climbers = movers_df[movers_df['rank_change'] > 0].nlargest(50, 'rank_change')

fig, ax = plt.subplots(figsize=(12, 10))
plot_data = top_climbers.sort_values('rank_change', ascending=True)
merchants = plot_data['merchant'].str[:35]
rank_changes = plot_data['rank_change']

bars = ax.barh(range(len(merchants)), rank_changes, color='#16a085', alpha=0.8, edgecolor='black', linewidth=0.5)
ax.set_yticks(range(len(merchants)))
ax.set_yticklabels([f"#{i+1} {m}" for i, m in enumerate(merchants)], fontsize=8)
ax.set_xlabel('Rank Positions Gained', fontsize=11, fontweight='bold')
ax.set_title('Personal Accounts - Top 50 Rank Climbers', fontsize=13, fontweight='bold', pad=15)

for i, (bar, val) in enumerate(zip(bars, rank_changes)):
    ax.text(val, bar.get_y() + bar.get_height()/2, f' ↑{int(val)}', va='center', fontsize=8, fontweight='bold')

ax.grid(axis='x', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.show()
print("="*120)
