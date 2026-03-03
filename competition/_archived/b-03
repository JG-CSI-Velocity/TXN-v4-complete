# ===========================================================================
# M6B-6a: BANK THREATS BY ACCOUNT PENETRATION
# ===========================================================================

print("\n" + "="*120)
print(" " * 40 + "M6B-6a: BANK THREATS BY ACCOUNT PENETRATION")
print("="*120)

if len(all_competitor_data) > 0:
    bank_categories = ['big_nationals', 'regionals', 'credit_unions', 'digital_banks']
    total_accounts = combined_df['primary_account_num'].nunique()
    
    penetration_data = []
    
    for competitor, competitor_trans in all_competitor_data.items():
        category = competitor_trans['competitor_category'].iloc[0]
        
        if category not in bank_categories:
            continue
        
        unique_accounts = competitor_trans['primary_account_num'].nunique()
        total_spend = competitor_trans['amount'].sum()
        transaction_count = len(competitor_trans)
        avg_spend_per_account = total_spend / unique_accounts if unique_accounts > 0 else 0
        
        penetration_pct = (unique_accounts / total_accounts) * 100
        
        penetration_data.append({
            'bank': competitor,
            'category': category,
            'unique_accounts': unique_accounts,
            'penetration_pct': penetration_pct,
            'total_spend': total_spend,
            'transaction_count': transaction_count,
            'avg_per_account': avg_spend_per_account
        })
    
    if len(penetration_data) > 0:
        pen_df = pd.DataFrame(penetration_data).sort_values('unique_accounts', ascending=False).head(15)
        
        display_df = pen_df.copy()
        display_df['category'] = display_df['category'].str.replace('_', ' ').str.title()
        display_df['unique_accounts'] = display_df['unique_accounts'].apply(lambda x: f"{x:,}")
        display_df['penetration_pct'] = display_df['penetration_pct'].apply(lambda x: f"{x:.2f}%")
        display_df['total_spend'] = display_df['total_spend'].apply(lambda x: f"${x:,.0f}")
        display_df['transaction_count'] = display_df['transaction_count'].apply(lambda x: f"{x:,}")
        display_df['avg_per_account'] = display_df['avg_per_account'].apply(lambda x: f"${x:,.0f}")
        
        display_df.columns = [
            'Bank', 'Category', 'Accounts', 'Penetration %', 
            'Total Spend', 'Transactions', 'Avg per Account'
        ]
        
        print("\nTop 15 Banks by Raw Account Penetration:")
        print("(Simple ranking by number of accounts captured)\n")
        display(display_df.style.hide(axis='index'))
        
        print("\n💡 Shows which banks have captured the most customer relationships")

print("="*120)
