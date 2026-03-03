# ===========================================================================
# VISUALIZATION: COMPETITOR SEGMENTATION BY CATEGORY
# ===========================================================================
"""
## Competitor Analysis - Segmentation by Category (Separate Charts)
"""

import matplotlib.pyplot as plt
import pandas as pd

# Group competitors by category
category_groups = {}

for competitor, comparison in competitor_spend_analysis.items():
    # Get category from the competitor data
    category = all_competitor_data[competitor]['competitor_category'].iloc[0]
    
    if category not in category_groups:
        category_groups[category] = []
    
    segment_counts = comparison['Segment'].value_counts()
    total = len(comparison)
    
    category_groups[category].append({
        'competitor': competitor,
        'total_accounts': total,
        'competitor_heavy': segment_counts.get('Competitor-Heavy', 0),
        'balanced': segment_counts.get('Balanced', 0),
        'cu_focused': segment_counts.get('CU-Focused', 0),
        'heavy_pct': segment_counts.get('Competitor-Heavy', 0) / total * 100,
        'balanced_pct': segment_counts.get('Balanced', 0) / total * 100,
        'cu_focused_pct': segment_counts.get('CU-Focused', 0) / total * 100
    })

# Create one chart per category
for category, competitors in category_groups.items():
    # Convert to DataFrame and sort by total accounts (descending)
    cat_df = pd.DataFrame(competitors)
    cat_df = cat_df.sort_values('total_accounts', ascending=True)  # Ascending for horizontal bars
    
    # Skip if no data
    if len(cat_df) == 0:
        continue
    
    # Take top 15 if more than 15
    if len(cat_df) > 15:
        cat_df = cat_df.tail(15)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, max(8, len(cat_df) * 0.5)))
    
    y_pos = range(len(cat_df))
    competitors = cat_df['competitor'].values
    
    # Create stacked bars
    p1 = ax.barh(y_pos, cat_df['heavy_pct'], 
                 color='#FF6B6B', label='Competitor-Heavy (>50%)', height=0.7)
    p2 = ax.barh(y_pos, cat_df['balanced_pct'], 
                 left=cat_df['heavy_pct'],
                 color='#FFA500', label='Balanced (25-50%)', height=0.7)
    p3 = ax.barh(y_pos, cat_df['cu_focused_pct'], 
                 left=cat_df['heavy_pct'] + cat_df['balanced_pct'],
                 color='#4ECDC4', label='CU-Focused (<25%)', height=0.7)
    
    # Customize
    ax.set_yticks(y_pos)
    ax.set_yticklabels(competitors, fontsize=10)
    ax.set_xlabel('Percentage of Accounts (%)', fontsize=12, fontweight='bold')
    
    # Format category name for title
    category_title = category.replace('_', ' ').title()
    ax.set_title(f'{category_title} - Account Segmentation (Top {len(cat_df)} by Total Accounts)', 
                 fontsize=14, fontweight='bold', pad=20)
    
    ax.legend(loc='lower right', fontsize=9)
    ax.set_xlim(0, 100)
    
    # Add grid
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Add account counts as text on the right
    for i, (idx, row) in enumerate(cat_df.iterrows()):
        ax.text(102, i, f"{int(row['total_accounts']):,}", 
                va='center', fontsize=9, fontweight='bold')
    
    # Add column header for account counts
    ax.text(102, len(cat_df), 'Accounts', 
            va='center', fontsize=9, fontweight='bold', style='italic')
    
    plt.tight_layout()
    plt.show()
    
    # Print summary for this category
    print(f"\n📊 {category_title} Summary:")
    print("="*80)
    print(f"  Total competitors: {len(cat_df)}")
    print(f"  Total accounts: {cat_df['total_accounts'].sum():,}")
    print(f"  Avg accounts per competitor: {cat_df['total_accounts'].mean():.0f}")
    
    # Calculate category-wide risk
    total_heavy = cat_df['competitor_heavy'].sum()
    total_balanced = cat_df['balanced'].sum()
    total_cu = cat_df['cu_focused'].sum()
    total_all = total_heavy + total_balanced + total_cu
    
    print(f"\n  Segmentation across category:")
    print(f"    🔴 Competitor-Heavy: {total_heavy:,} ({total_heavy/total_all*100:.1f}%)")
    print(f"    🟠 Balanced: {total_balanced:,} ({total_balanced/total_all*100:.1f}%)")
    print(f"    🔵 CU-Focused: {total_cu:,} ({total_cu/total_all*100:.1f}%)")
    print("="*80)

print("\n✓ Category-specific segmentation visualizations complete")
