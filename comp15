# ===========================================================================
# M6B-6d: MATERIAL THREATS (BALANCED VIEW)
# ===========================================================================

print("\n" + "="*120)
print(" " * 40 + "M6B-6d: MATERIAL THREATS (BALANCED VIEW)")
print("="*120)

if len(all_competitor_data) > 0:
    bank_categories = ['big_nationals', 'regionals', 'credit_unions', 'digital_banks']
    total_accounts = combined_df['primary_account_num'].nunique()
    
    # Set minimum thresholds for "material" threats
    MIN_ACCOUNTS = 100  # Must have at least 100 accounts
    MIN_SPEND = 50000   # Must have at least $50K in spend
    
    material_data = []
    
    for competitor, competitor_trans in all_competitor_data.items():
        category = competitor_trans['competitor_category'].iloc[0]
        
        if category not in bank_categories:
            continue
        
        unique_accounts = competitor_trans['primary_account_num'].nunique()
        total_spend = competitor_trans['amount'].sum()
        
        # Filter out immaterial competitors
        if unique_accounts < MIN_ACCOUNTS or total_spend < MIN_SPEND:
            continue
        
        penetration_pct = (unique_accounts / total_accounts) * 100
        
        # Calculate growth if enough data
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
        
        # Balanced threat score
        # 50% = Account penetration (market share)
        # 50% = Total spend (absolute dollars at risk)
        # Growth rate shown separately, not in score
        
        threat_score = (
            (penetration_pct * 5) +  # 50% weight
            (total_spend / 100000) * 5  # 50% weight
        )
        
        material_data.append({
            'bank': competitor,
            'category': category,
            'unique_accounts': unique_accounts,
            'penetration_pct': penetration_pct,
            'total_spend': total_spend,
            'growth_rate': growth_rate,
            'threat_score': threat_score
        })
    
    if len(material_data) > 0:
        material_df = pd.DataFrame(material_data).sort_values('threat_score', ascending=False).head(15)
        
        display_df = material_df.copy()
        display_df['category'] = display_df['category'].str.replace('_', ' ').str.title()
        display_df['unique_accounts'] = display_df['unique_accounts'].apply(lambda x: f"{x:,}")
        display_df['penetration_pct'] = display_df['penetration_pct'].apply(lambda x: f"{x:.2f}%")
        display_df['total_spend'] = display_df['total_spend'].apply(lambda x: f"${x:,.0f}")
        display_df['growth_rate'] = display_df['growth_rate'].apply(lambda x: f"{x:+.1f}%")
        display_df['threat_score'] = display_df['threat_score'].apply(lambda x: f"{x:.1f}")
        
        display_df.columns = [
            'Bank', 'Category', 'Accounts', 'Penetration', 
            'Total Spend', 'Growth (6mo)', 'Threat Score'
        ]
        
        print("\nTop 15 Material Bank Threats:")
        print(f"Minimum Thresholds: {MIN_ACCOUNTS:,} accounts AND ${MIN_SPEND:,} spend")
        print("Threat Score = 50% Penetration + 50% Total Spend (Growth shown separately)\n")
        display(display_df.style.hide(axis='index'))
        
        print("\n💡 Filters out small players - focuses on banks with meaningful market presence")
        print("   High score = Significant market share + Large absolute dollars at risk")
    else:
        print(f"\n⚠ No banks meet minimum thresholds ({MIN_ACCOUNTS} accounts, ${MIN_SPEND} spend)")

print("="*120)
