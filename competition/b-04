# ===========================================================================
# M6B-6b: BANK THREATS BY TOTAL SPEND
# ===========================================================================

print("\n" + "="*120)
print(" " * 40 + "M6B-6b: BANK THREATS BY TOTAL SPEND")
print("="*120)

if len(all_competitor_data) > 0:
    bank_categories = ['big_nationals', 'regionals', 'credit_unions', 'digital_banks']
    
    spend_data = []
    
    for competitor, competitor_trans in all_competitor_data.items():
        category = competitor_trans['competitor_category'].iloc[0]
        
        if category not in bank_categories:
            continue
        
        total_spend = competitor_trans['amount'].sum()
        unique_accounts = competitor_trans['primary_account_num'].nunique()
        transaction_count = len(competitor_trans)
        avg_transaction = total_spend / transaction_count if transaction_count > 0 else 0
        
        spend_data.append({
            'bank': competitor,
            'category': category,
            'total_spend': total_spend,
            'unique_accounts': unique_accounts,
            'transaction_count': transaction_count,
            'avg_transaction': avg_transaction
        })
    
    if len(spend_data) > 0:
        spend_df = pd.DataFrame(spend_data).sort_values('total_spend', ascending=False).head(15)
        
        display_df = spend_df.copy()
        display_df['category'] = display_df['category'].str.replace('_', ' ').str.title()
        display_df['total_spend'] = display_df['total_spend'].apply(lambda x: f"${x:,.0f}")
        display_df['unique_accounts'] = display_df['unique_accounts'].apply(lambda x: f"{x:,}")
        display_df['transaction_count'] = display_df['transaction_count'].apply(lambda x: f"{x:,}")
        display_df['avg_transaction'] = display_df['avg_transaction'].apply(lambda x: f"${x:,.2f}")
        
        display_df.columns = [
            'Bank', 'Category', 'Total Spend', 'Accounts', 
            'Transactions', 'Avg Transaction'
        ]
        
        print("\nTop 15 Banks by Total Spend:")
        print("(Follow the money - where is the most spend going?)\n")
        display(display_df.style.hide(axis='index'))
        
        print("\n💡 Shows which banks are capturing the most transaction volume in dollars")

print("="*120)
