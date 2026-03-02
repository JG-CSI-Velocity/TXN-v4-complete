# ===========================================================================
# M6B-5: MONTHLY TREND ANALYSIS
# ===========================================================================

print("\n" + "="*120)
print(" " * 40 + "M6B-5: MONTHLY TREND ANALYSIS")
print("="*120)

if len(all_competitor_data) > 0:
    # Combine all competitor transactions
    all_competitor_trans = pd.concat(all_competitor_data.values(), ignore_index=True)
    
    # Add year_month if not present
    if 'year_month' not in all_competitor_trans.columns:
        all_competitor_trans['year_month'] = pd.to_datetime(all_competitor_trans['transaction_date']).dt.to_period('M')
    
    monthly_trends = all_competitor_trans.groupby('year_month').agg({
        'amount': ['sum', 'count'],
        'primary_account_num': 'nunique'
    }).round(2)
    
    monthly_trends.columns = ['Total Spend', 'Transaction Count', 'Unique Accounts']
    monthly_trends = monthly_trends.sort_index()
    
    # Calculate month-over-month growth
    monthly_trends['Spend Growth %'] = monthly_trends['Total Spend'].pct_change() * 100
    monthly_trends['Transaction Growth %'] = monthly_trends['Transaction Count'].pct_change() * 100
    
    # Format for display
    monthly_display = monthly_trends.copy()
    monthly_display.index = monthly_display.index.astype(str)
    monthly_display['Total Spend'] = monthly_display['Total Spend'].apply(lambda x: f"${x:,.0f}")
    monthly_display['Transaction Count'] = monthly_display['Transaction Count'].apply(lambda x: f"{int(x):,}")
    monthly_display['Unique Accounts'] = monthly_display['Unique Accounts'].apply(lambda x: f"{int(x):,}")
    monthly_display['Spend Growth %'] = monthly_display['Spend Growth %'].apply(
        lambda x: f"{x:+.1f}%" if pd.notna(x) else "-"
    )
    monthly_display['Transaction Growth %'] = monthly_display['Transaction Growth %'].apply(
        lambda x: f"{x:+.1f}%" if pd.notna(x) else "-"
    )
    
    display(monthly_display)

print("="*120)
