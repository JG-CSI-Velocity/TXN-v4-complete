# ===========================================================================
# M1B - TOP 50 MERCHANTS BY TRANSACTION COUNT
# ===========================================================================
"""
## M1B: Top 50 Merchants by Transaction Count (Consolidated)
"""

top_by_transactions = combined_df.groupby('merchant_consolidated').agg({
    'amount': ['sum', 'count', 'mean'],
    'primary_account_num': 'nunique'
}).round(2)

top_by_transactions.columns = ['total_amount', 'transaction_count', 'avg_transaction', 'unique_accounts']
top_by_transactions = top_by_transactions.sort_values('transaction_count', ascending=False).head(50)

# Format for display
display_df = top_by_transactions.reset_index()
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
print(" " * 30 + "TOP 50 MERCHANTS BY TRANSACTION COUNT")
print("="*100)

display(display_df)

# Summary stats
total_spend = top_by_transactions['total_amount'].sum()
total_transactions = top_by_transactions['transaction_count'].sum()
total_accounts = top_by_transactions['unique_accounts'].sum()

summary = pd.DataFrame({
    'Metric': ['Total Spend (Top 50)', 'Total Transactions (Top 50)', 'Total Unique Accounts (Top 50)'],
    'Value': [f"${total_spend:,.0f}", f"{total_transactions:,.0f}", f"{total_accounts:,.0f}"]
})

print("\n")
display(summary)
print("="*100)
