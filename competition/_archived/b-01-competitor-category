# ===========================================================================
# M6B-6: TOP COMPETITOR BY CATEGORY
# ===========================================================================

print("\n" + "="*120)
print(" " * 40 + "M6B-6: TOP COMPETITOR IN EACH CATEGORY")
print("="*120)

if len(all_competitor_data) > 0:
    summary_df = pd.DataFrame(summary_data)
    
    # Get top competitor per category
    top_by_category = summary_df.loc[summary_df.groupby('category')['total_amount'].idxmax()].copy()
    
    # Add market context
    category_totals = summary_df.groupby('category')['total_amount'].sum()
    top_by_category['category_total'] = top_by_category['category'].map(category_totals)
    top_by_category['market_share_pct'] = (top_by_category['total_amount'] / top_by_category['category_total'] * 100)
    
    # Format for display
    display_df = top_by_category[['category', 'competitor', 'total_amount', 'unique_accounts', 'market_share_pct']].copy()
    display_df = display_df.sort_values('total_amount', ascending=False)
    
    display_df['category'] = display_df['category'].str.replace('_', ' ').str.title()
    display_df['total_amount'] = display_df['total_amount'].apply(lambda x: f"${x:,.0f}")
    display_df['unique_accounts'] = display_df['unique_accounts'].apply(lambda x: f"{x:,}")
    display_df['market_share_pct'] = display_df['market_share_pct'].apply(lambda x: f"{x:.1f}%")
    
    display_df.columns = ['Category', 'Top Competitor', 'Total Spend', 'Unique Accounts', '% of Category']
    
    print("\n")
    display(display_df.style.hide(axis='index'))
    
    print("\n💡 Insight: Shows the dominant competitor in each competitive category")

print("="*120)
