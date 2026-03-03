# ===========================================================================
# M2B - TOP 50 MERCHANT CATEGORIES (MCC) BY TRANSACTION COUNT
# ===========================================================================
"""
## M2B: Top 50 Merchant Categories by Transaction Count
"""

top_mcc_by_trans = combined_df.groupby('mcc_code').agg({
    'amount': ['sum', 'count', 'mean'],
    'primary_account_num': 'nunique',
    'merchant_name': 'nunique'
}).round(2)

top_mcc_by_trans.columns = ['total_amount', 'transaction_count', 'avg_transaction', 'unique_accounts', 'num_merchants']
top_mcc_by_trans = top_mcc_by_trans.sort_values('transaction_count', ascending=False).head(50)

# Format for display
display_df = top_mcc_by_trans.reset_index()
display_df = display_df.rename(columns={
    'mcc_code': 'MCC Code',
    'transaction_count': 'Transactions',
    'unique_accounts': 'Unique Accounts',
    'num_merchants': 'Merchants',
    'total_amount': 'Total Spend',
    'avg_transaction': 'Avg Transaction'
})

# Format columns
display_df['Total Spend'] = display_df['Total Spend'].apply(lambda x: f"${x:,.0f}")
display_df['Avg Transaction'] = display_df['Avg Transaction'].apply(lambda x: f"${x:.2f}")

print("\n" + "="*110)
print(" " * 30 + "TOP 50 MERCHANT CATEGORIES BY TRANSACTION COUNT")
print("="*110)

display(display_df)

# Summary stats
total_spend = top_mcc_by_trans['total_amount'].sum()
total_transactions = top_mcc_by_trans['transaction_count'].sum()
total_accounts = top_mcc_by_trans['unique_accounts'].sum()

summary = pd.DataFrame({
    'Metric': [
        'Total Transactions (Top 50)', 
        'Total Spend (Top 50)', 
        'Total Unique Accounts (Top 50)'
    ],
    'Value': [
        f"{total_transactions:,.0f}", 
        f"${total_spend:,.0f}",
        f"{total_accounts:,.0f}"
    ]
})

print("\n")
display(summary)
print("="*110)
