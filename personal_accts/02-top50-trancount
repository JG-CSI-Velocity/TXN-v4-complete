# ===========================================================================
# M4B - TOP 50 PERSONAL MERCHANTS BY TRANSACTION COUNT
# ===========================================================================
"""
## M4B: Top 50 Personal Merchants by Transaction Count (Consolidated)
"""

top_personal_trans = personal_df.groupby('merchant_consolidated').agg({
    'amount': ['sum', 'count', 'mean'],
    'primary_account_num': 'nunique'
}).round(2)

top_personal_trans.columns = ['total_amount', 'transaction_count', 'avg_transaction', 'unique_accounts']
top_personal_trans = top_personal_trans.sort_values('transaction_count', ascending=False).head(50)

# Format for display
display_df = top_personal_trans.reset_index()
display_df = display_df.rename(columns={
    'merchant_consolidated': 'Merchant',
    'transaction_count': 'Transactions',
    'total_amount': 'Total Spend',
    'avg_transaction': 'Avg Transaction',
    'unique_accounts': 'Unique Accounts'
})

# Format columns
display_df['Total Spend'] = display_df['Total Spend'].apply(lambda x: f"${x:,.0f}")
display_df['Avg Transaction'] = display_df['Avg Transaction'].apply(lambda x: f"${x:.2f}")

print("\n" + "="*100)
print(" " * 28 + "TOP 50 PERSONAL MERCHANTS BY TRANSACTION COUNT")
print("="*100)

display(display_df.style.hide(axis='index'))

# Summary stats
total_spend = top_personal_trans['total_amount'].sum()
total_transactions = top_personal_trans['transaction_count'].sum()
total_accounts = top_personal_trans['unique_accounts'].sum()

summary = pd.DataFrame({
    'Metric': [
        'Total Transactions (Top 50)',
        'Total Spend (Top 50)',
        'Total Personal Accounts (Top 50)'
    ],
    'Value': [
        f"{total_transactions:,.0f}",
        f"${total_spend:,.0f}",
        f"{total_accounts:,.0f}"
    ]
})

print("\n")
display(summary.style.hide(axis='index'))
print("="*100)
