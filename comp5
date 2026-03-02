# ===========================================================================
# M6B-1: HIGH-LEVEL METRICS
# ===========================================================================

print("\n" + "="*120)
print(" " * 40 + "M6B-1: HIGH-LEVEL COMPETITOR METRICS")
print("="*120)

if len(all_competitor_data) == 0:
    print("\n⚠ No competitor data to analyze")
else:
    summary_df = pd.DataFrame(summary_data)
    summary_df = summary_df.sort_values('total_amount', ascending=False)
    
    total_competitor_trans = summary_df['total_transactions'].sum()
    total_competitor_spend = summary_df['total_amount'].sum()
    total_competitor_accounts = summary_df['unique_accounts'].sum()
    total_competitors_found = len(all_competitor_data)
    
    # Calculate as % of overall dataset
    total_all_trans = len(combined_df)
    total_all_spend = combined_df['amount'].sum()
    total_all_accounts = combined_df['primary_account_num'].nunique()
    
    pct_trans = (total_competitor_trans / total_all_trans * 100) if total_all_trans > 0 else 0
    pct_spend = (total_competitor_spend / total_all_spend * 100) if total_all_spend > 0 else 0
    pct_accounts = (total_competitor_accounts / total_all_accounts * 100) if total_all_accounts > 0 else 0
    
    metrics_summary = pd.DataFrame({
        'Metric': [
            'Competitors Found',
            '',
            'Total Competitor Transactions',
            '% of All Transactions',
            '',
            'Total Competitor Spend',
            '% of All Spend',
            '',
            'Unique Accounts Using Competitors',
            '% of All Accounts',
            '',
            'Avg Spend per Competitor Account',
            'Avg Transactions per Competitor Account'
        ],
        'Value': [
            f"{total_competitors_found:,}",
            '',
            f"{total_competitor_trans:,}",
            f"{pct_trans:.2f}%",
            '',
            f"${total_competitor_spend:,.2f}",
            f"{pct_spend:.2f}%",
            '',
            f"{total_competitor_accounts:,}",
            f"{pct_accounts:.2f}%",
            '',
            f"${total_competitor_spend / total_competitor_accounts:,.2f}" if total_competitor_accounts > 0 else "$0.00",
            f"{total_competitor_trans / total_competitor_accounts:.1f}" if total_competitor_accounts > 0 else "0.0"
        ]
    })
    
    display(metrics_summary.style.hide(axis='index'))

print("="*120)
