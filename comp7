# ===========================================================================
# M6B-3: CATEGORY BREAKDOWN
# ===========================================================================

print("\n" + "="*120)
print(" " * 40 + "M6B-3: BREAKDOWN BY CATEGORY")
print("="*120)

if len(all_competitor_data) > 0:
    summary_df = pd.DataFrame(summary_data)
    
    category_summary = summary_df.groupby('category').agg({
        'total_transactions': 'sum',
        'unique_accounts': 'sum',
        'total_amount': 'sum',
        'competitor': 'count'
    }).sort_values('total_amount', ascending=False)
    
    category_summary.columns = ['Total Transactions', 'Total Accounts', 'Total Spend', 'Competitor Count']
    
    # Add percentages
    category_summary['% of Competitor Spend'] = (
        category_summary['Total Spend'] / category_summary['Total Spend'].sum() * 100
    )
    category_summary['Avg per Competitor'] = (
        category_summary['Total Spend'] / category_summary['Competitor Count']
    )
    
    category_display = category_summary.copy()
    category_display.index = category_display.index.str.replace('_', ' ').str.title()
    category_display['Total Transactions'] = category_display['Total Transactions'].apply(lambda x: f"{int(x):,}")
    category_display['Total Accounts'] = category_display['Total Accounts'].apply(lambda x: f"{int(x):,}")
    category_display['Total Spend'] = category_display['Total Spend'].apply(lambda x: f"${x:,.0f}")
    category_display['% of Competitor Spend'] = category_display['% of Competitor Spend'].apply(lambda x: f"{x:.1f}%")
    category_display['Avg per Competitor'] = category_display['Avg per Competitor'].apply(lambda x: f"${x:,.0f}")
    
    display(category_display)

print("="*120)
