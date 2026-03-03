# ===========================================================================
# COMPETITOR SPEND ANALYSIS - ACCOUNT SEGMENTATION
# ===========================================================================
"""
## Creates competitor_spend_analysis dictionary for segmentation
Analyzes what % of each account's spend goes to each competitor
"""

print("\n" + "="*120)
print(" " * 40 + "ANALYZING COMPETITOR SPEND BY ACCOUNT")
print("="*120)

if len(all_competitor_data) == 0:
    print("\n⚠ No competitor data found - run M6A detection first!")
else:
    competitor_spend_analysis = {}
    
    # Get total spend per account (for percentage calculations)
    account_totals = combined_df.groupby('primary_account_num')['amount'].sum()
    
    print(f"\nAnalyzing spend patterns for {len(all_competitor_data)} competitors...")
    
    for competitor, competitor_trans in all_competitor_data.items():
        # Get spend per account for this competitor
        competitor_spend_by_account = competitor_trans.groupby('primary_account_num')['amount'].sum()
        
        # Create comparison dataframe
        comparison = pd.DataFrame({
            'account': competitor_spend_by_account.index,
            'competitor_spend': competitor_spend_by_account.values
        })
        
        # Add total spend for each account
        comparison['total_spend'] = comparison['account'].map(account_totals)
        
        # Calculate percentage
        comparison['competitor_pct'] = (comparison['competitor_spend'] / comparison['total_spend'] * 100)
        
        # Segment accounts
        comparison['Segment'] = pd.cut(
            comparison['competitor_pct'],
            bins=[0, 25, 50, 100],
            labels=['CU-Focused', 'Balanced', 'Competitor-Heavy'],
            include_lowest=True
        )
        
        # Store in dictionary
        competitor_spend_analysis[competitor] = comparison
    
    print(f"✓ Analysis complete for {len(competitor_spend_analysis)} competitors")
    
    # Quick summary
    total_heavy = sum(len(df[df['Segment'] == 'Competitor-Heavy']) for df in competitor_spend_analysis.values())
    total_balanced = sum(len(df[df['Segment'] == 'Balanced']) for df in competitor_spend_analysis.values())
    total_cu = sum(len(df[df['Segment'] == 'CU-Focused']) for df in competitor_spend_analysis.values())
    
    print(f"\nOverall Segmentation:")
    print(f"  • Competitor-Heavy accounts: {total_heavy:,}")
    print(f"  • Balanced accounts: {total_balanced:,}")
    print(f"  • CU-Focused accounts: {total_cu:,}")

print("="*120)
