# ===========================================================================
# M6B-6: BANK COMPETITIVE THREAT ASSESSMENT
# ===========================================================================

print("\n" + "="*120)
print(" " * 40 + "M6B-6: BANK COMPETITIVE THREAT ASSESSMENT")
print("="*120)

if len(all_competitor_data) > 0:
    threat_data = []
    
    # ONLY assess threats from actual banks
    bank_categories = ['big_nationals', 'regionals', 'credit_unions', 'digital_banks']
    
    # Get total accounts for penetration calculation
    total_accounts = combined_df['primary_account_num'].nunique()
    
    for competitor, competitor_trans in all_competitor_data.items():
        category = competitor_trans['competitor_category'].iloc[0]
        
        # Skip if not a bank
        if category not in bank_categories:
            continue
        
        total_spend = competitor_trans['amount'].sum()
        unique_accounts = competitor_trans['primary_account_num'].nunique()
        
        # Account penetration (% of total accounts using this competitor)
        penetration_pct = (unique_accounts / total_accounts) * 100
        
        # Calculate recent growth (last 3 months vs previous 3 months)
        if 'year_month' not in competitor_trans.columns:
            competitor_trans['year_month'] = pd.to_datetime(competitor_trans['transaction_date']).dt.to_period('M')
        
        sorted_months = sorted(competitor_trans['year_month'].unique())
        
        if len(sorted_months) >= 6:
            recent_3 = sorted_months[-3:]
            previous_3 = sorted_months[-6:-3]
            
            recent_spend = competitor_trans[competitor_trans['year_month'].isin(recent_3)]['amount'].sum()
            previous_spend = competitor_trans[competitor_trans['year_month'].isin(previous_3)]['amount'].sum()
            
            growth_rate = ((recent_spend - previous_spend) / previous_spend * 100) if previous_spend > 0 else 0
        else:
            growth_rate = 0
        
        # Threat Score = Weighted combination
        # 40% = Account penetration (how many accounts they've captured)
        # 30% = Total spend (how much money is at risk)
        # 30% = Growth rate (are they gaining momentum?)
        
        threat_score = (
            (penetration_pct * 4) +  # Weight: 40%
            (total_spend / 100000) * 3 +  # Weight: 30%
            (max(growth_rate, 0) / 10) * 3  # Weight: 30% (only positive growth)
        )
        
        threat_data.append({
            'competitor': competitor,
            'category': category,
            'total_spend': total_spend,
            'unique_accounts': unique_accounts,
            'penetration_pct': penetration_pct,
            'growth_rate': growth_rate,
            'threat_score': threat_score
        })
    
    if len(threat_data) > 0:
        threat_df = pd.DataFrame(threat_data).sort_values('threat_score', ascending=False).head(15)
        
        # Format for display
        display_df = threat_df.copy()
        display_df['category'] = display_df['category'].str.replace('_', ' ').str.title()
        display_df['total_spend'] = display_df['total_spend'].apply(lambda x: f"${x:,.0f}")
        display_df['unique_accounts'] = display_df['unique_accounts'].apply(lambda x: f"{x:,}")
        display_df['penetration_pct'] = display_df['penetration_pct'].apply(lambda x: f"{x:.2f}%")
        display_df['growth_rate'] = display_df['growth_rate'].apply(lambda x: f"{x:+.1f}%")
        display_df['threat_score'] = display_df['threat_score'].apply(lambda x: f"{x:.1f}")
        
        display_df.columns = [
            'Bank', 'Category', 'Total Spend', 'Accounts', 
            'Penetration', 'Growth (6mo)', 'Threat Score'
        ]
        
        print("\nTop 15 Bank Competitive Threats:")
        print("Threat Score = 40% Penetration + 30% Total Spend + 30% Growth Rate")
        print("(Excludes wallets/P2P/BNPL - those are threats to banking itself, not direct competitors)\n")
        display(display_df.style.hide(axis='index'))
        
        print("\n💡 Highest threat = High account penetration + Large spend + Growing momentum")
    else:
        print("\n⚠ No bank competitors found in dataset")

print("="*120)
