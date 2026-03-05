# ===========================================================================
# M6B-7: NON-BANK THREATS TO BANKING RELATIONSHIP
# ===========================================================================

print("\n" + "="*120)
print(" " * 40 + "M6B-7: NON-BANK THREATS TO BANKING RELATIONSHIP")
print("="*120)

if len(all_competitor_data) > 0:
    # These aren't competing banks - they're replacing banking functions
    non_bank_categories = ['wallets_p2p', 'bnpl']
    
    # Get total accounts
    total_accounts = combined_df['primary_account_num'].nunique()
    total_spend = combined_df['amount'].sum()
    
    non_bank_data = []
    
    for competitor, competitor_trans in all_competitor_data.items():
        category = competitor_trans['competitor_category'].iloc[0]
        
        # Only look at non-bank threats
        if category not in non_bank_categories:
            continue
        
        comp_spend = competitor_trans['amount'].sum()
        unique_accounts = competitor_trans['primary_account_num'].nunique()
        transaction_count = len(competitor_trans)
        
        # Penetration
        penetration_pct = (unique_accounts / total_accounts) * 100
        
        # % of total spend going through this service
        spend_share = (comp_spend / total_spend) * 100
        
        non_bank_data.append({
            'service': competitor,
            'category': category,
            'total_spend': comp_spend,
            'unique_accounts': unique_accounts,
            'transaction_count': transaction_count,
            'penetration_pct': penetration_pct,
            'spend_share': spend_share
        })
    
    if len(non_bank_data) > 0:
        non_bank_df = pd.DataFrame(non_bank_data).sort_values('total_spend', ascending=False)
        
        # Format for display
        display_df = non_bank_df.copy()
        display_df['category'] = display_df['category'].str.replace('_', ' ').str.title()
        display_df['total_spend'] = display_df['total_spend'].apply(lambda x: f"${x:,.0f}")
        display_df['unique_accounts'] = display_df['unique_accounts'].apply(lambda x: f"{x:,}")
        display_df['transaction_count'] = display_df['transaction_count'].apply(lambda x: f"{x:,}")
        display_df['penetration_pct'] = display_df['penetration_pct'].apply(lambda x: f"{x:.2f}%")
        display_df['spend_share'] = display_df['spend_share'].apply(lambda x: f"{x:.2f}%")
        
        display_df.columns = [
            'Service', 'Type', 'Total Spend', 'Accounts', 
            'Transactions', 'Account Penetration', '% of Total Spend'
        ]
        
        print("\nServices Replacing Traditional Banking Functions:\n")
        display(display_df.style.hide(axis='index'))
        
        # Summary stats
        total_non_bank_spend = non_bank_df['total_spend'].sum()
        total_non_bank_accounts = non_bank_df['unique_accounts'].sum()
        
        print(f"\n💡 KEY INSIGHTS:")
        print(f"   • Combined non-bank spend: ${total_non_bank_spend:,.0f}")
        print(f"   • Total account relationships: {total_non_bank_accounts:,}")
        print(f"   • These services handle payments, transfers, and credit traditionally done by banks")
        print(f"   • High penetration = customers finding alternatives to traditional banking")
    else:
        print("\n⚠ No non-bank services found in dataset")

print("="*120)
