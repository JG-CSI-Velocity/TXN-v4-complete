# ===========================================================================
# M4C VISUALIZATION - Top 25 Personal Merchants by Unique Accounts
# ===========================================================================

fig, ax = plt.subplots(figsize=(12, 10))

# Get top 25 and reverse order so #1 is at top
top_25 = top_personal_accounts.head(25).iloc[::-1]

merchants = [m[:40] + '...' if len(m) > 40 else m for m in top_25.index]
values = top_25['unique_accounts'].values

# Color gradient
colors = plt.cm.RdPu(np.linspace(0.5, 0.9, 25))

bars = ax.barh(range(25), values, color=colors, edgecolor='black', linewidth=0.8)
ax.set_yticks(range(25))
ax.set_yticklabels(merchants, fontsize=10)
ax.set_xlabel('Unique Personal Account Count', fontsize=12, fontweight='bold')
ax.set_title('Top 25 Personal Merchants by Account Count', fontsize=14, fontweight='bold', pad=20)

# Add value labels
for i, (bar, value) in enumerate(zip(bars, values)):
    ax.text(value + max(values)*0.01, bar.get_y() + bar.get_height()/2, 
            f'{int(value):,}', va='center', fontsize=9, fontweight='bold')

# Format x-axis
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e3:.1f}K' if x >= 1000 else f'{x:.0f}'))
ax.grid(axis='x', linestyle='--', alpha=0.3)
ax.set_axisbelow(True)

# Add rank labels on left side
for i, rank in enumerate(range(25, 0, -1)):
    ax.text(-max(values)*0.02, i, f'#{rank}', 
            ha='right', va='center', fontsize=9, fontweight='bold', color='gray')

plt.tight_layout()
plt.show()
