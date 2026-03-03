# ===========================================================================
# M1 - TOP 50 MERCHANTS BY TOTAL SPEND
# ===========================================================================
"""
## M1: Top 50 Merchants by Total Spend (Consolidated)
"""

top_merchants_overall = combined_df.groupby('merchant_consolidated').agg({
    'amount': ['sum', 'count', 'mean'],
    'primary_account_num': 'nunique'
}).round(2)

top_merchants_overall.columns = ['total_amount', 'transaction_count', 'avg_transaction', 'unique_accounts']
top_merchants_overall = top_merchants_overall.sort_values('total_amount', ascending=False).head(50)

# Format for display
display_df = top_merchants_overall.reset_index()
display_df = display_df.rename(columns={
    'merchant_consolidated': 'Merchant',
    'total_amount': 'Total Spend',
    'transaction_count': 'Transactions',
    'avg_transaction': 'Avg Transaction',
    'unique_accounts': 'Unique Accounts'
})

# Format currency columns
display_df['Total Spend'] = display_df['Total Spend'].apply(lambda x: f"${x:,.0f}")
display_df['Avg Transaction'] = display_df['Avg Transaction'].apply(lambda x: f"${x:.2f}")

print("\n" + "="*100)
print(" " * 35 + "TOP 50 MERCHANTS BY TOTAL SPEND")
print("="*100)

display(display_df)

# Summary stats
total_spend = top_merchants_overall['total_amount'].sum()
total_transactions = top_merchants_overall['transaction_count'].sum()
total_accounts = top_merchants_overall['unique_accounts'].sum()

summary = pd.DataFrame({
    'Metric': ['Total Spend (Top 50)', 'Total Transactions (Top 50)', 'Total Unique Accounts (Top 50)'],
    'Value': [f"${total_spend:,.0f}", f"{total_transactions:,.0f}", f"{total_accounts:,.0f}"]
})

print("\n")
display(summary)
print("="*100)
