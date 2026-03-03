# ===========================================================================
# M2A - TOP 50 MERCHANT CATEGORIES (MCC) BY UNIQUE ACCOUNTS
# ===========================================================================
"""
## M2A: Top 50 Merchant Categories by Unique Account Count
Based on MCC (Merchant Category Code) groupings
"""

top_mcc_by_accounts = combined_df.groupby('mcc_code').agg({
    'amount': ['sum', 'count', 'mean'],
    'primary_account_num': 'nunique',
    'merchant_name': 'nunique'
}).round(2)

top_mcc_by_accounts.columns = ['total_amount', 'transaction_count', 'avg_transaction', 'unique_accounts', 'num_merchants']
top_mcc_by_accounts = top_mcc_by_accounts.sort_values('unique_accounts', ascending=False).head(50)

# Format for display
display_df = top_mcc_by_accounts.reset_index()
display_df = display_df.rename(columns={
    'mcc_code': 'MCC Code',
    'unique_accounts': 'Unique Accounts',
    'num_merchants': 'Merchants',
    'transaction_count': 'Transactions',
    'total_amount': 'Total Spend',
    'avg_transaction': 'Avg Transaction'
})

# Format columns
display_df['Total Spend'] = display_df['Total Spend'].apply(lambda x: f"${x:,.0f}")
display_df['Avg Transaction'] = display_df['Avg Transaction'].apply(lambda x: f"${x:.2f}")

print("\n" + "="*110)
print(" " * 30 + "TOP 50 MERCHANT CATEGORIES BY UNIQUE ACCOUNT COUNT")
print(" " * 40 + "(Based on MCC Codes)")
print("="*110)

display(display_df)

# Summary stats
total_spend = top_mcc_by_accounts['total_amount'].sum()
total_transactions = top_mcc_by_accounts['transaction_count'].sum()
total_accounts = top_mcc_by_accounts['unique_accounts'].sum()
total_merchants = top_mcc_by_accounts['num_merchants'].sum()

summary = pd.DataFrame({
    'Metric': [
        'Total MCC Categories (Top 50)', 
        'Total Unique Accounts (Top 50)', 
        'Total Merchants (Top 50)',
        'Total Transactions (Top 50)', 
        'Total Spend (Top 50)'
    ],
    'Value': [
        f"{len(top_mcc_by_accounts)}",
        f"{total_accounts:,.0f}",
        f"{total_merchants:,.0f}",
        f"{total_transactions:,.0f}", 
        f"${total_spend:,.0f}"
    ]
})

print("\n")
display(summary)
print("="*110)
