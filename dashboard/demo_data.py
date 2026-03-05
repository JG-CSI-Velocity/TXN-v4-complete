"""Comprehensive synthetic demo data for all 23 notebook sections."""

import numpy as np
import pandas as pd

np.random.seed(42)

# =========================================================================
# GLOBAL CONSTANTS
# =========================================================================
MONTHS = pd.date_range('2025-01-01', '2026-01-01', freq='MS')
MONTH_LABELS = [d.strftime('%b%y') for d in MONTHS]
N_ACCOUNTS = 33_205
N_TRANSACTIONS = 5_885_334
HOURS = list(range(24))
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# =========================================================================
# 01 - GENERAL / PORTFOLIO
# =========================================================================
_base_txns = np.linspace(420_000, 460_000, len(MONTHS)) + np.random.normal(0, 8000, len(MONTHS))
_base_spend = np.linspace(38_000_000, 42_000_000, len(MONTHS)) + np.random.normal(0, 500_000, len(MONTHS))
_base_active = np.linspace(28_000, 29_500, len(MONTHS)) + np.random.normal(0, 200, len(MONTHS))

monthly_trend = pd.DataFrame({
    'month': MONTHS, 'label': MONTH_LABELS,
    'transactions': _base_txns.astype(int),
    'spend': _base_spend.round(0),
    'active_accounts': _base_active.astype(int),
    'avg_txn': (_base_spend / _base_txns).round(2),
})

tier_dist = pd.DataFrame({
    'tier': ['Power', 'Heavy', 'Moderate', 'Light', 'Dormant'],
    'accounts': [2987, 5640, 9300, 10120, 5158],
    'pct': [9.0, 17.0, 28.0, 30.5, 15.5],
    'avg_monthly_spend': [2850, 1420, 680, 210, 15],
    'avg_monthly_txns': [85, 48, 25, 8, 0.5],
})

age_dist = pd.DataFrame({
    'age_band': ['18-25', '26-35', '36-45', '46-55', '56-65', '65+'],
    'accounts': [3100, 6200, 7500, 6800, 5500, 4105],
    'avg_spend': [380, 720, 950, 880, 640, 420],
    'avg_txns': [18, 32, 42, 38, 28, 19],
})

acct_age_dist = pd.DataFrame({
    'band': ['1-90d', '91-180d', '181-365d', '1-2yr', '2-3yr', '3-5yr', '5-10yr', '10-20yr', '20yr+'],
    'accounts': [1200, 1800, 3200, 4500, 3800, 5200, 6100, 4800, 2605],
    'avg_spend': [180, 320, 480, 620, 710, 820, 890, 780, 550],
})

# Spend brackets
bracket_dist = pd.DataFrame({
    'bracket': ['< $1', '$1-5', '$5-10', '$10-25', '$25-50', '$50-100', '$100-500', '$500+'],
    'txn_count': [320_000, 680_000, 820_000, 1_200_000, 980_000, 750_000, 680_000, 455_334],
    'pct_txns': [5.4, 11.6, 13.9, 20.4, 16.6, 12.7, 11.6, 7.7],
    'total_spend': [120_000, 2_100_000, 6_200_000, 21_000_000, 36_000_000, 52_000_000, 148_000_000, 233_000_000],
})

# Hourly heatmap data
hourly_heatmap = np.random.uniform(0.2, 1.0, (7, 24))
hourly_heatmap[0:5, 8:18] *= 2.5   # weekday business hours
hourly_heatmap[5:7, 10:20] *= 2.0  # weekend midday
hourly_heatmap = (hourly_heatmap / hourly_heatmap.max() * 100).round(1)

# Seasonal index
seasonal_index = pd.DataFrame({
    'month': MONTH_LABELS,
    'index': [88, 92, 98, 95, 100, 102, 105, 103, 97, 108, 118, 115, 90],
})

# Growth scorecard
growth_metrics = pd.DataFrame({
    'metric': ['Active Accounts', 'Total Spend', 'Avg Txn/Acct', 'Merchant Diversity',
               'Power Tier %', 'New Account Activation'],
    'current': ['29,500', '$42M/mo', '177', '18.3/acct', '9.0%', '68%'],
    'change': ['+3.2%', '+8.1%', '+4.7%', '+1.2', '+0.5pp', '+4pp'],
    'status': ['Green', 'Green', 'Green', 'Amber', 'Amber', 'Green'],
})

# =========================================================================
# 02 - MERCHANT
# =========================================================================
top_merchants = pd.DataFrame({
    'merchant': ['Amazon', 'Walmart', 'Target', 'Costco', 'Shell', 'Chevron',
                 'McDonald\'s', 'Starbucks', 'Home Depot', 'Kroger',
                 'Safeway', 'Walgreens', 'CVS', 'Netflix', 'Spotify',
                 'Apple', 'Uber', 'DoorDash', 'T-Mobile', 'Verizon'],
    'total_spend': [18.5, 12.3, 8.7, 7.2, 6.8, 5.5, 4.2, 3.9, 3.6, 3.4,
                    2.8, 2.2, 1.9, 1.6, 1.1, 2.4, 2.1, 1.8, 1.5, 1.3],
    'total_txns': [620, 480, 310, 180, 420, 380, 350, 410, 95, 280,
                   220, 190, 160, 280, 240, 150, 200, 180, 120, 110],
    'unique_accounts': [22.0, 18.5, 14.2, 8.9, 16.0, 14.5, 15.8, 13.2, 5.6, 12.4,
                        10.8, 11.2, 10.5, 18.0, 14.5, 9.8, 8.2, 7.5, 6.8, 6.2],
    'growth_pct': [12, 5, 8, 15, -3, -5, 2, 18, 6, 1, -2, 3, -1, 22, 28, 14, 35, 42, 8, 5],
    'volatility': [0.08, 0.05, 0.07, 0.12, 0.15, 0.14, 0.06, 0.09, 0.18, 0.04,
                   0.05, 0.06, 0.04, 0.03, 0.02, 0.07, 0.22, 0.25, 0.06, 0.05],
})

merchant_by_age = pd.DataFrame({
    'merchant': ['Amazon', 'Walmart', 'Target', 'Starbucks', 'Netflix'] * 6,
    'age_band': sorted(['18-25', '26-35', '36-45', '46-55', '56-65', '65+'] * 5),
    'spend_share': np.random.uniform(5, 25, 30).round(1),
})

# =========================================================================
# 03 - MCC CATEGORIES
# =========================================================================
mcc_categories = pd.DataFrame({
    'category': ['Grocery', 'Gas/Fuel', 'Restaurants', 'General Merch', 'Healthcare',
                 'Utilities', 'Travel', 'Entertainment', 'Auto', 'Insurance',
                 'Clothing', 'Home Improvement', 'Electronics', 'Education', 'Subscriptions'],
    'total_spend': [82, 48, 42, 38, 28, 24, 22, 18, 16, 14, 12, 11, 9, 7, 5],
    'total_txns': [1200, 680, 520, 380, 210, 180, 95, 280, 85, 60, 150, 75, 65, 40, 320],
    'unique_accounts': [28.5, 22.1, 20.4, 16.8, 12.3, 15.2, 6.8, 18.5, 5.2, 8.4,
                        12.1, 6.5, 8.8, 3.2, 22.0],
    'avg_txn_size': [68, 71, 42, 85, 133, 128, 232, 28, 188, 245, 80, 142, 138, 175, 14],
})

# =========================================================================
# 04/05 - BUSINESS / PERSONAL ACCOUNTS
# =========================================================================
biz_personal_split = pd.DataFrame({
    'type': ['Business', 'Personal'],
    'accounts': [4_820, 28_385],
    'total_spend': [148_000_000, 350_000_000],
    'avg_spend': [2550, 950],
    'avg_txns': [68, 32],
})

biz_top_merchants = pd.DataFrame({
    'merchant': ['Amazon Business', 'Office Depot', 'Costco Business', 'Home Depot', 'Staples',
                 'FedEx', 'UPS', 'Sam\'s Club', 'Lowe\'s', 'Grainger'],
    'total_spend': [8.2, 4.1, 3.8, 3.5, 2.8, 2.4, 2.1, 1.9, 1.7, 1.5],
    'total_txns': [120, 85, 45, 52, 68, 95, 88, 35, 42, 28],
})

personal_top_merchants = pd.DataFrame({
    'merchant': ['Amazon', 'Walmart', 'Target', 'Shell', 'Starbucks',
                 'McDonald\'s', 'Kroger', 'Costco', 'Netflix', 'Chevron'],
    'total_spend': [14.2, 10.8, 7.5, 5.8, 3.6, 3.8, 3.2, 4.1, 1.5, 4.2],
    'total_txns': [520, 420, 280, 380, 390, 330, 260, 150, 270, 340],
})

# =========================================================================
# 06 - COMPETITION
# =========================================================================
competitor_data = pd.DataFrame({
    'competitor': ['Chase', 'Bank of America', 'Wells Fargo', 'Capital One', 'Citi',
                   'US Bank', 'Discover', 'American Express'],
    'accounts_using': [8200, 6100, 4800, 3900, 2100, 1800, 1500, 1200],
    'wallet_share': [18.5, 14.2, 11.8, 9.1, 5.2, 4.1, 3.5, 2.8],
    'avg_competitor_spend': [620, 480, 540, 390, 310, 280, 250, 420],
    'monthly_trend': [1.2, 0.8, -0.3, 2.1, 0.5, -0.2, 1.8, 0.4],
    'threat_score': [92, 78, 65, 72, 45, 38, 55, 48],
})

# Competitor by segment
comp_by_segment = pd.DataFrame({
    'segment': ['Power', 'Heavy', 'Moderate', 'Light', 'Dormant'],
    'pct_with_competitor': [42, 55, 62, 48, 22],
    'avg_wallet_share': [12, 18, 24, 15, 8],
})

# =========================================================================
# 07 - FINANCIAL SERVICES
# =========================================================================
finsvc_categories = pd.DataFrame({
    'category': ['Banking/ATM', 'Insurance', 'Investment', 'Lending', 'Tax Services',
                 'Real Estate', 'Accounting'],
    'accounts': [18200, 8400, 5200, 3800, 2100, 1500, 800],
    'total_spend': [42, 14, 8.5, 6.2, 3.8, 2.4, 1.2],
    'avg_monthly': [192, 139, 136, 136, 151, 133, 125],
})

finsvc_top_merchants = pd.DataFrame({
    'merchant': ['Chase ATM', 'State Farm', 'Geico', 'Allstate', 'Charles Schwab',
                 'Fidelity', 'Progressive', 'H&R Block', 'TurboTax', 'Edward Jones'],
    'accounts': [8500, 4200, 3100, 2800, 2400, 1800, 2200, 1200, 1800, 900],
    'total_spend': [12.4, 4.8, 3.2, 2.9, 3.8, 2.4, 2.1, 1.5, 0.8, 1.2],
})

# =========================================================================
# 08 - ICS ACQUISITION
# =========================================================================
ics_channels = pd.DataFrame({
    'channel': ['Branch Referral', 'Online Application', 'Direct Mail', 'Phone', 'Partner'],
    'accounts': [4200, 3800, 2100, 1500, 800],
    'activation_rate': [78, 65, 52, 48, 71],
    'avg_first_month_spend': [420, 380, 280, 250, 350],
    '90day_retention': [88, 82, 68, 62, 75],
})

# =========================================================================
# 09 - CAMPAIGN (ARS)
# =========================================================================
campaign_summary = pd.DataFrame({
    'metric': ['Total Mailed', 'Responders', 'Non-Responders', 'Response Rate',
               'Avg Lift/Responder', 'Cumulative Protected Spend'],
    'value': ['12,400', '3,720', '8,680', '30.0%', '$142/mo', '$6.3M'],
})

campaign_by_wave = pd.DataFrame({
    'wave': ['TH10', 'TH15', 'TH20', 'TH25', 'NU5+'],
    'mailed': [2800, 2400, 2200, 2000, 3000],
    'responded': [980, 780, 620, 540, 800],
    'response_rate': [35.0, 32.5, 28.2, 27.0, 26.7],
    'avg_lift': [168, 152, 138, 124, 142],
})

cohort_lift = pd.DataFrame({
    'month': MONTH_LABELS,
    'responder_spend': np.linspace(820, 980, len(MONTHS)) + np.random.normal(0, 20, len(MONTHS)),
    'non_responder_spend': np.linspace(680, 690, len(MONTHS)) + np.random.normal(0, 15, len(MONTHS)),
    'counterfactual': np.linspace(680, 720, len(MONTHS)) + np.random.normal(0, 10, len(MONTHS)),
})

# =========================================================================
# 10 - BRANCH
# =========================================================================
branch_data = pd.DataFrame({
    'branch': [f'Branch {i}' for i in range(1, 16)],
    'accounts': np.random.randint(1200, 4500, 15),
    'total_spend': np.random.uniform(2_000_000, 12_000_000, 15).round(0),
    'avg_txns': np.random.uniform(22, 48, 15).round(1),
    'pct_business': np.random.uniform(8, 22, 15).round(1),
    'avg_balance': np.random.uniform(3000, 8000, 15).round(0),
})
branch_data = branch_data.sort_values('total_spend', ascending=False).reset_index(drop=True)

# =========================================================================
# 11 - TRANSACTION TYPE
# =========================================================================
txn_type_split = pd.DataFrame({
    'type': ['Signature', 'PIN', 'Contactless', 'Online', 'Recurring'],
    'txn_count': [2_800_000, 1_200_000, 680_000, 820_000, 385_334],
    'total_spend': [285_000_000, 98_000_000, 52_000_000, 48_000_000, 15_000_000],
    'avg_txn': [101.79, 81.67, 76.47, 58.54, 38.93],
    'pct_txns': [47.6, 20.4, 11.6, 13.9, 6.5],
})

# =========================================================================
# 12 - PRODUCT
# =========================================================================
product_dist = pd.DataFrame({
    'product': ['Platinum Rewards', 'Gold', 'Classic', 'Student', 'Business Platinum',
                'Business Gold', 'Secured', 'Other'],
    'accounts': [8200, 7500, 6800, 2400, 3200, 1800, 1500, 1805],
    'avg_spend': [1420, 980, 620, 280, 2850, 1680, 180, 450],
    'avg_txns': [48, 35, 22, 12, 72, 45, 8, 18],
})

# =========================================================================
# 13 - ATTRITION
# =========================================================================
attrition_tiers = pd.DataFrame({
    'tier': ['Stable', 'Slowing', 'Declining', 'Dormant'],
    'accounts': [21_480, 5_643, 2_840, 3_242],
    'pct': [64.7, 17.0, 8.5, 9.8],
    'avg_velocity': [1.05, 0.78, 0.42, 0.05],
    'avg_spend_at_risk': [0, 4200, 8800, 1200],
})

# =========================================================================
# 14 - BALANCE
# =========================================================================
balance_bands = pd.DataFrame({
    'band': ['$0', '$1-500', '$500-2K', '$2K-5K', '$5K-10K', '$10K-25K', '$25K-50K', '$50K+'],
    'accounts': [2720, 4800, 6200, 7100, 5400, 4200, 1800, 985],
    'total_balance': [0, 1.2, 7.4, 24.8, 40.5, 63.0, 58.5, 82.4],
    'avg_spend': [15, 180, 420, 680, 920, 1100, 1280, 1450],
})

pfi_tiers = pd.DataFrame({
    'tier': ['Primary', 'Secondary', 'Tertiary', 'Incidental'],
    'accounts': [6100, 8400, 9200, 9505],
    'pct': [18.4, 25.3, 27.7, 28.6],
    'avg_balance': [12400, 6800, 3200, 980],
    'avg_spend': [1680, 920, 480, 180],
})

# =========================================================================
# 15 - INTERCHANGE
# =========================================================================
interchange_monthly = pd.DataFrame({
    'month': MONTH_LABELS,
    'pin_revenue': np.linspace(120_000, 135_000, len(MONTHS)) + np.random.normal(0, 3000, len(MONTHS)),
    'sig_revenue': np.linspace(200_000, 230_000, len(MONTHS)) + np.random.normal(0, 5000, len(MONTHS)),
    'sig_ratio': np.linspace(62, 72, len(MONTHS)) + np.random.normal(0, 1.5, len(MONTHS)),
})

pin_heavy_accounts = pd.DataFrame({
    'segment': ['Heavy PIN (>80%)', 'Moderate PIN (50-80%)', 'Balanced', 'Moderate SIG (50-80%)', 'Heavy SIG (>80%)'],
    'accounts': [4200, 5800, 6400, 8200, 8605],
    'opportunity': [420_000, 180_000, 0, 0, 0],
})

# =========================================================================
# 16 - REG E / OVERDRAFT
# =========================================================================
rege_trend = pd.DataFrame({
    'month': MONTH_LABELS,
    'opted_in': np.linspace(10_200, 11_400, len(MONTHS)).astype(int) + np.random.randint(-100, 100, len(MONTHS)),
    'opted_out': np.linspace(23_005, 21_805, len(MONTHS)).astype(int) + np.random.randint(-100, 100, len(MONTHS)),
})

od_limit_dist = pd.DataFrame({
    'limit_band': ['$0-200', '$200-500', '$500-1000', '$1000-2000', '$2000+'],
    'accounts': [3200, 4100, 2800, 800, 500],
    'avg_usage': [42, 28, 18, 12, 8],
})

# =========================================================================
# 17 - PAYROLL
# =========================================================================
payroll_summary = pd.DataFrame({
    'metric': ['Accounts w/ Payroll', 'Detection Rate', 'Avg Payroll Deposit',
               'Monthly Frequency', 'Biweekly Frequency'],
    'value': ['9,340', '28.1%', '$2,480', '62%', '38%'],
})

payroll_processors = pd.DataFrame({
    'processor': ['ADP', 'Direct Deposit (Generic)', 'Paychex', 'Gusto', 'Workday',
                  'Recurring Credit Pattern', 'Paylocity', 'Other'],
    'accounts': [2800, 2400, 1200, 800, 600, 520, 480, 540],
    'avg_deposit': [2850, 2200, 2680, 1950, 3200, 1800, 2400, 2100],
})

# =========================================================================
# 18 - RELATIONSHIP
# =========================================================================
product_cross_sell = pd.DataFrame({
    'product_count': [1, 2, 3, 4, '5+'],
    'accounts': [11_560, 9_200, 6_800, 3_400, 2_245],
    'avg_spend': [280, 620, 980, 1450, 2100],
    'avg_balance': [1200, 3800, 6400, 9200, 14800],
    'churn_risk': [18.5, 8.2, 4.1, 2.3, 1.2],
})

next_best_product = pd.DataFrame({
    'current_products': ['Checking Only', 'Checking + Savings', 'Checking + CC',
                         'Full Suite', 'Business Only'],
    'recommended': ['Credit Card', 'Credit Card', 'Auto Loan', 'Investment', 'Payroll'],
    'propensity': [0.42, 0.38, 0.28, 0.22, 0.35],
    'accounts_eligible': [4800, 3200, 2400, 1800, 1200],
})

# =========================================================================
# 19 - SEGMENT EVOLUTION
# =========================================================================
seg_order = ['Power', 'Heavy', 'Moderate', 'Light', 'Dormant']
seg_migration = np.array([
    [82, 12, 4, 1.5, 0.5],
    [8, 72, 14, 5, 1],
    [2, 10, 70, 14, 4],
    [0.5, 3, 12, 68, 16.5],
    [0.2, 0.8, 3, 12, 84],
])

seg_net_flow = pd.DataFrame({
    'segment': seg_order,
    'upgraded': [0, 238, 930, 1263, 396],
    'degraded': [538, 1128, 1674, 1981, 0],
    'net': [-538, -890, -744, -718, 396],
    'net_pct': [-18.0, -15.8, -8.0, -7.1, 7.7],
})

# =========================================================================
# 20 - RETENTION
# =========================================================================
retention_funnel = pd.DataFrame({
    'status': ['Active', 'Cooling', 'Dormant', 'Closed'],
    'accounts': [24_200, 4_100, 3_650, 1_255],
    'annual_spend': [380_000_000, 28_000_000, 2_100_000, 0],
    'color': ['#34D399', '#FBBF24', '#FB923C', '#F87171'],
})

retention_by_tier = pd.DataFrame({
    'tier': ['Power', 'Heavy', 'Moderate', 'Light', 'Dormant'],
    'churn_rate': [1.2, 2.8, 4.1, 6.5, 12.3],
    'at_risk_pct': [5.2, 12.4, 18.8, 24.2, 42.0],
})

# =========================================================================
# 21 - ENGAGEMENT MIGRATION
# =========================================================================
migration_matrix = pd.DataFrame(seg_migration, index=seg_order, columns=seg_order)

migration_monthly = pd.DataFrame({
    'month': MONTH_LABELS,
    'upgrades': np.random.randint(300, 600, len(MONTHS)),
    'downgrades': np.random.randint(200, 500, len(MONTHS)),
})
migration_monthly['net'] = migration_monthly['upgrades'] - migration_monthly['downgrades']

# =========================================================================
# 22 - EXECUTIVE SCORECARD
# =========================================================================
scorecard_data = [
    {'category': 'Attrition',     'metric': '% Accounts At Risk',     'value': '18.3%',  'trend': 'down', 'rag': 'Amber'},
    {'category': 'Attrition',     'metric': 'Annual Spend at Risk',   'value': '$4.2M',  'trend': 'down', 'rag': 'Amber'},
    {'category': 'Balance',       'metric': 'Total Deposits',         'value': '$182M',  'trend': 'up',   'rag': 'Green'},
    {'category': 'Balance',       'metric': 'Average Balance',        'value': '$5,480', 'trend': 'flat', 'rag': 'Green'},
    {'category': 'Balance',       'metric': '% Zero-Balance',         'value': '8.2%',   'trend': 'flat', 'rag': 'Green'},
    {'category': 'Interchange',   'metric': 'Est. Annual IC',         'value': '$3.8M',  'trend': 'up',   'rag': 'Green'},
    {'category': 'Interchange',   'metric': 'SIG Ratio',              'value': '72.4%',  'trend': 'up',   'rag': 'Green'},
    {'category': 'Interchange',   'metric': 'PIN-to-SIG Opportunity', 'value': '$420K',  'trend': 'up',   'rag': 'Amber'},
    {'category': 'Reg E',         'metric': 'Opt-In Rate',            'value': '34.2%',  'trend': 'up',   'rag': 'Amber'},
    {'category': 'Reg E',         'metric': 'Avg OD Limit',           'value': '$680',   'trend': 'flat', 'rag': 'Green'},
    {'category': 'Payroll',       'metric': '% With Payroll/DD',      'value': '28.1%',  'trend': 'flat', 'rag': 'Amber'},
    {'category': 'Payroll',       'metric': '% Primary PFI',          'value': '18.4%',  'trend': 'flat', 'rag': 'Amber'},
    {'category': 'Relationship',  'metric': 'Avg Products/Member',    'value': '2.31',   'trend': 'flat', 'rag': 'Amber'},
    {'category': 'Relationship',  'metric': '% Single-Product',       'value': '34.8%',  'trend': 'flat', 'rag': 'Amber'},
    {'category': 'Segmentation',  'metric': '% Upgraded',             'value': '12.3%',  'trend': 'up',   'rag': 'Amber'},
    {'category': 'Segmentation',  'metric': '% Degraded',             'value': '8.7%',   'trend': 'flat', 'rag': 'Green'},
    {'category': 'Retention',     'metric': '% At Risk',              'value': '22.1%',  'trend': 'flat', 'rag': 'Amber'},
    {'category': 'Retention',     'metric': 'Closed Account Rate',    'value': '3.8%',   'trend': 'flat', 'rag': 'Green'},
    {'category': 'Retention',     'metric': 'Spend at Risk',          'value': '$6.1M',  'trend': 'down', 'rag': 'Red'},
    {'category': 'Engagement',    'metric': 'Net Migration/Month',    'value': '+142',   'trend': 'up',   'rag': 'Green'},
    {'category': 'Engagement',    'metric': 'Power Tier Growth',      'value': '+2.1%',  'trend': 'up',   'rag': 'Green'},
    {'category': 'Engagement',    'metric': 'Dormant Tier Growth',    'value': '-1.4%',  'trend': 'down', 'rag': 'Green'},
]
scorecard_df = pd.DataFrame(scorecard_data)

# =========================================================================
# STRUCTURED REPLACEMENTS for inline np.random placeholders
# =========================================================================

# -- Merchant monthly trends (replaces random in 03, 05, 06) --
_merch_top5 = ['Amazon', 'Walmart', 'Target', 'Costco', 'Starbucks']
_merch_bases = [1.42, 0.95, 0.67, 0.55, 0.30]
_seasonal = np.array([0.88, 0.92, 0.98, 0.95, 1.00, 1.02, 1.05, 1.03, 0.97, 1.08, 1.18, 1.15, 0.90])
merchant_monthly_trend = pd.DataFrame({'month': MONTH_LABELS})
for m, base in zip(_merch_top5, _merch_bases):
    merchant_monthly_trend[m] = (base * _seasonal * 1_000_000 + np.random.normal(0, base * 30_000, len(MONTHS))).round(0)

# -- Business merchant monthly trends --
_biz_top3 = ['Amazon Business', 'Office Depot', 'Costco Business']
_biz_bases = [0.63, 0.32, 0.29]
biz_merchant_monthly = pd.DataFrame({'month': MONTH_LABELS})
for m, base in zip(_biz_top3, _biz_bases):
    biz_merchant_monthly[m] = (base * _seasonal * 1_000_000 + np.random.normal(0, base * 20_000, len(MONTHS))).round(0)

# -- Personal merchant monthly trends --
personal_merchant_monthly = pd.DataFrame({'month': MONTH_LABELS})
_pers_top3 = ['Amazon', 'Walmart', 'Target']
_pers_bases = [1.08, 0.82, 0.58]
for m, base in zip(_pers_top3, _pers_bases):
    personal_merchant_monthly[m] = (base * _seasonal * 1_000_000 + np.random.normal(0, base * 25_000, len(MONTHS))).round(0)

# -- MCC monthly trends (replaces random in 04) --
mcc_monthly_trend = pd.DataFrame({'month': MONTH_LABELS})
_mcc_top4 = ['Grocery', 'Gas/Fuel', 'Restaurants', 'General Merch']
_mcc_bases = [6.3, 3.7, 3.2, 2.9]
for cat, base in zip(_mcc_top4, _mcc_bases):
    mcc_monthly_trend[cat] = (base * _seasonal * 1_000_000 + np.random.normal(0, base * 40_000, len(MONTHS))).round(0)

# -- MCC age heatmap (replaces random in 04) --
mcc_age_heatmap = np.array([
    [28, 22, 18, 12, 8],     # 18-25: grocery heavy, less insurance
    [25, 20, 22, 15, 10],    # 26-35
    [22, 18, 20, 18, 14],    # 36-45
    [20, 15, 16, 22, 18],    # 46-55
    [24, 14, 12, 20, 22],    # 56-65
    [28, 12, 8, 18, 25],     # 65+: grocery + healthcare
], dtype=float)

# -- MCC seasonal heatmap (replaces random in 04) --
mcc_seasonal_heatmap = np.array([
    [95, 92, 98, 96, 100, 102, 104, 103, 98, 105, 112, 108],  # Grocery
    [102, 98, 95, 92, 98, 105, 112, 108, 95, 92, 88, 85],     # Gas/Fuel
    [88, 90, 95, 98, 102, 108, 115, 112, 100, 105, 118, 125],  # Restaurants
    [85, 88, 92, 90, 95, 98, 100, 98, 95, 110, 128, 135],      # General Merch
    [105, 98, 95, 92, 90, 88, 85, 88, 92, 98, 102, 108],       # Healthcare
], dtype=float)

# -- Bracket volatility (replaces random in 02) --
bracket_volatility = np.array([0.22, 0.15, 0.12, 0.08, 0.10, 0.14, 0.18, 0.25])

# -- Bracket trend (replaces random in 02) --
bracket_trend = pd.DataFrame({'month': MONTH_LABELS})
_br_labels = ['< $1', '$10-25', '$100-500', '$500+']
_br_bases = [24_000, 92_000, 52_000, 35_000]
for br, base in zip(_br_labels, _br_bases):
    _growth = np.linspace(1.0, 1.08, len(MONTHS))
    bracket_trend[br] = (base * _growth * _seasonal + np.random.normal(0, base * 0.02, len(MONTHS))).round(0).astype(int)

# -- Age x time heatmap (replaces random in 02) --
age_time_heatmap = np.array([
    [5.2, 22.5, 18.8, 12.5],   # 18-25: evening heavy
    [8.1, 18.2, 20.5, 10.2],   # 26-35
    [12.4, 22.1, 15.2, 6.3],   # 36-45: afternoon peak
    [14.8, 24.5, 12.1, 4.6],   # 46-55: morning/afternoon
    [16.2, 22.8, 8.5, 3.5],    # 56-65: morning heavy
    [18.5, 20.2, 5.8, 2.5],    # 65+: morning dominant
], dtype=float)

# -- Competitor monthly trend (replaces random in 07) --
competitor_monthly_trend = pd.DataFrame({'month': MONTH_LABELS})
_comp_names = ['Chase', 'Bank of America', 'Capital One']
_comp_bases = [8200, 6100, 3900]
for comp, base in zip(_comp_names, _comp_bases):
    _trend = np.linspace(base, base * 1.06, len(MONTHS))
    competitor_monthly_trend[comp] = (_trend + np.random.normal(0, base * 0.015, len(MONTHS))).round(0).astype(int)

# -- Competitor segment heatmap (replaces random in 07) --
competitor_segment_heatmap = np.array([
    [42, 28, 18, 8, 5],      # Chase: heavy in Power/Heavy
    [35, 32, 22, 12, 8],     # BofA
    [28, 25, 28, 15, 10],    # Wells Fargo
    [22, 30, 32, 18, 12],    # Capital One: moderate-focused
    [15, 18, 22, 20, 15],    # Citi
], dtype=float)

# -- FinSvc structured data (replaces random in 08) --
finsvc_recency_heatmap = np.array([
    [85, 62, 45, 28, 18, 12, 8],    # Banking/ATM: high recency
    [42, 38, 52, 65, 72, 78, 82],   # Insurance: annual patterns
    [28, 32, 35, 42, 48, 55, 62],   # Investment: growing
    [35, 28, 22, 18, 15, 12, 10],   # Lending: front-loaded
    [15, 12, 18, 22, 32, 58, 82],   # Tax: seasonal
], dtype=float)

finsvc_monthly_trend = pd.DataFrame({'month': MONTH_LABELS})
_finsvc_cats = ['Banking/ATM', 'Insurance', 'Investment', 'Lending']
_finsvc_bases = [3.2, 1.1, 0.65, 0.48]
for cat, base in zip(_finsvc_cats, _finsvc_bases):
    finsvc_monthly_trend[cat] = (base * _seasonal * 1_000_000 + np.random.normal(0, base * 50_000, len(MONTHS))).round(0)

finsvc_leakage = pd.DataFrame({
    'tier': ['Power', 'Heavy', 'Moderate', 'Light', 'Dormant'],
    'leakage_pct': [55, 48, 38, 22, 8],
    'leakage_spend': [4.2, 3.8, 2.8, 1.2, 0.2],
})

finsvc_biz_personal = pd.DataFrame({
    'category': ['Banking/ATM', 'Insurance', 'Investment', 'Lending', 'Tax'],
    'business_pct': [22, 35, 28, 42, 48],
    'personal_pct': [78, 65, 72, 58, 52],
})

# -- ICS monthly trend (replaces random in 09) --
ics_monthly_trend = pd.DataFrame({
    'month': MONTH_LABELS,
    'branch_referral': np.linspace(280, 380, len(MONTHS)).astype(int) + np.random.randint(-15, 15, len(MONTHS)),
    'online': np.linspace(240, 350, len(MONTHS)).astype(int) + np.random.randint(-20, 20, len(MONTHS)),
    'direct_mail': np.linspace(180, 160, len(MONTHS)).astype(int) + np.random.randint(-10, 10, len(MONTHS)),
})

# -- Branch structured data (replaces random in 11) --
_top_branches = branch_data['branch'].head(8).tolist()
_top_merchants_short = ['Amazon', 'Walmart', 'Target', 'Shell', 'Starbucks']
branch_merchant_heatmap = np.array([
    [22, 15, 12, 8, 6],
    [18, 18, 14, 10, 5],
    [20, 12, 15, 12, 8],
    [15, 20, 10, 14, 4],
    [12, 16, 18, 6, 10],
    [25, 10, 8, 15, 3],
    [14, 14, 12, 8, 12],
    [10, 22, 16, 5, 8],
], dtype=float)

branch_monthly_trend = pd.DataFrame({'month': MONTH_LABELS})
for i, br in enumerate(_top_branches[:5]):
    _base = branch_data.iloc[i]['total_spend'] / 12
    branch_monthly_trend[br] = (_base * _seasonal + np.random.normal(0, _base * 0.03, len(MONTHS))).round(0)

# -- Transaction type trend (replaces random in 12) --
txn_type_trend = pd.DataFrame({'month': MONTH_LABELS})
txn_type_trend['Signature'] = np.linspace(44, 49, len(MONTHS)) + np.random.normal(0, 0.5, len(MONTHS))
txn_type_trend['PIN'] = np.linspace(24, 20, len(MONTHS)) + np.random.normal(0, 0.4, len(MONTHS))
txn_type_trend['Contactless'] = np.linspace(8, 14, len(MONTHS)) + np.random.normal(0, 0.3, len(MONTHS))
txn_type_trend['Online'] = np.linspace(12, 15, len(MONTHS)) + np.random.normal(0, 0.3, len(MONTHS))

# -- Product monthly trends (replaces random in 13) --
product_monthly_trend = pd.DataFrame({'month': MONTH_LABELS})
_prod_top3 = ['Platinum Rewards', 'Gold', 'Classic']
_prod_bases = [9.8, 6.2, 3.5]
for prod, base in zip(_prod_top3, _prod_bases):
    product_monthly_trend[prod] = (base * _seasonal * 1_000_000 + np.random.normal(0, base * 30_000, len(MONTHS))).round(0)

# -- Product x merchant heatmap (replaces random in 13) --
product_merchant_heatmap = np.array([
    [25, 18, 15, 12, 8],    # Platinum Rewards
    [20, 20, 14, 10, 6],    # Gold
    [18, 22, 12, 8, 5],     # Classic
    [12, 15, 18, 14, 10],   # Student
    [28, 10, 8, 18, 4],     # Business Platinum
], dtype=float)

# -- Interchange merchant SIG heatmap (replaces random in 16) --
interchange_merchant_sig = np.array([
    [82, 78, 72, 65, 58],   # Amazon: high SIG
    [75, 70, 68, 62, 55],   # Walmart
    [88, 85, 80, 72, 65],   # Target
    [35, 38, 42, 48, 52],   # Shell: low SIG (gas pumps)
    [92, 88, 85, 78, 72],   # Starbucks: very high SIG
], dtype=float)

# -- Segment projection (replaces random in 20) --
_seg_counts = [2987, 5640, 9300, 10120, 5158]
segment_projection = pd.DataFrame({'month': [f'Month {i}' for i in range(1, 7)]})
_seg_deltas = [12, -15, -8, -5, 16]  # per-month net change
for seg, base, delta in zip(seg_order, _seg_counts, _seg_deltas):
    _proj = np.array([base + delta * i for i in range(1, 7)]) + np.random.randint(-20, 20, 6)
    segment_projection[seg] = _proj

# -- Campaign swipe comparison (replaces random in 10) --
campaign_swipe_comparison = np.array([
    [65, 58, 52, 48, 42],   # 3-month responders
    [42, 38, 35, 32, 28],   # 3-month non-responders
    [72, 65, 60, 55, 48],   # 12-month responders
    [48, 42, 38, 35, 30],   # 12-month non-responders
], dtype=float)

# -- Sankey flow data for attrition cascade --
sankey_sources = [0, 0, 1, 1, 2, 2, 3]
sankey_targets = [1, 4, 2, 4, 3, 4, 4]
sankey_values = [4100, 24200, 3650, 1255, 800, 2850, 455]
sankey_labels = ['Active (24,200)', 'Cooling (4,100)', 'Dormant (3,650)',
                 'Closed (1,255)', 'Retained']
