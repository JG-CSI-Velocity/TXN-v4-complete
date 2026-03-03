# ===========================================================================
# M6B-6c: FASTEST GROWING BANKS (MOMENTUM)
# ===========================================================================

print("\n" + "="*120)
print(" " * 40 + "M6B-6c: FASTEST GROWING BANKS (MOMENTUM)")
print("="*120)

if len(all_competitor_data) > 0:
    bank_categories = ['big_nationals', 'regionals', 'credit_unions', 'digital_banks']
    
    growth_data = []
    
    for competitor, competitor_trans in all_competitor_data.items():
        category = competitor_trans['competitor_category'].iloc[0]
        
        if category not in bank_categories:
            continue
        
        # Ensure year_month exists
        if 'year_month' not in competitor_trans.columns:
            competitor_trans['year_month'] = pd.to_datetime(competitor_trans['transaction_date']).dt.to_period('M')
        
        sorted_months = sorted(competitor_trans['year_month'].unique())
        
        # Need at least 6 months to calculate growth
        if len(sorted_months) < 6:
            continue
        
        recent_3 = sorted_months[-3:]
        previous_3 = sorted_months[-6:-3]
        
        recent_spend = competitor_trans[competitor_trans['year_month'].isin(recent_3)]['amount'].sum()
        previous_spend = competitor_trans[competitor_trans['year_month'].isin(previous_3)]['amount'].sum()
        
        recent_accounts = competitor_trans[competitor_trans['year_month'].isin(recent_3)]['primary_account_num'].nunique()
        previous_accounts = competitor_trans[competitor_trans['year_month'].isin(previous_3)]['primary_account_num'].nunique()
        
        spend_growth = ((recent_spend - previous_spend) / previous_spend * 100) if previous_spend > 0 else 0
        account_growth = ((recent_accounts - previous_accounts) / previous_accounts * 100) if previous_accounts > 0 else 0
        
        # Only show positive growth
        if spend_growth > 0:
            growth_data.append({
                'bank': competitor,
                'category': category,
                'spend_growth': spend_growth,
                'account_growth': account_growth,
                'recent_spend': recent_spend,
                'recent_accounts': recent_accounts,
                'previous_spend': previous_spend
            })
    
    if len(growth_data) > 0:
        growth_df = pd.DataFrame(growth_data).sort_values('spend_growth', ascending=False).head(15)
        
        display_df = growth_df.copy()
        display_df['category'] = display_df['category'].str.replace('_', ' ').str.title()
        display_df['spend_growth'] = display_df['spend_growth'].apply(lambda x: f"{x:+.1f}%")
        display_df['account_growth'] = display_df['account_growth'].apply(lambda x: f"{x:+.1f}%")
        display_df['recent_spend'] = display_df['recent_spend'].apply(lambda x: f"${x:,.0f}")
        display_df['previous_spend'] = display_df['previous_spend'].apply(lambda x: f"${x:,.0f}")
        display_df['recent_accounts'] = display_df['recent_accounts'].apply(lambda x: f"{x:,}")
        
        display_df.columns = [
            'Bank', 'Category', 'Spend Growth', 'Account Growth', 
            'Recent Spend (3mo)', 'Accounts (Recent)', 'Previous Spend (3mo)'
        ]
        
        print("\nTop 15 Fastest Growing Banks:")
        print("(Last 3 months vs previous 3 months)\n")
        display(display_df.style.hide(axis='index'))
        
        print("\n💡 Shows which banks are gaining momentum - growing spend and accounts")
        print("⚠️ Note: Small banks can show high % growth from low base")
    else:
        print("\n⚠ Insufficient data to calculate growth rates (need 6+ months)")

print("="*120)
