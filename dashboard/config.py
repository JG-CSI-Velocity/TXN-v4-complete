# -- Dark-mode executive palette --
GEN_COLORS = {
    'primary':   '#6EE7B7',   # mint green - primary accent
    'accent':    '#F87171',   # coral red - alerts/danger
    'success':   '#34D399',   # emerald
    'warning':   '#FBBF24',   # amber
    'info':      '#60A5FA',   # sky blue
    'light_bg':  '#111827',   # card surface
    'dark_text': '#E2E8F0',   # slate 200
    'muted':     '#94A3B8',   # slate 400 (WCAG AA safe on #0B1120)
    'grid':      '#1E293B',   # slate 800
    'surface':   '#0B1120',   # deepest bg
    'card':      '#1E293B',   # card bg
    'glow':      '#6EE7B7',   # glow accent
}

ENGAGE_PALETTE = {
    'Power':    '#F87171',
    'Heavy':    '#FBBF24',
    'Moderate': '#34D399',
    'Light':    '#60A5FA',
    'Dormant':  '#64748B',
}
ENGAGE_ORDER = ['Power', 'Heavy', 'Moderate', 'Light', 'Dormant']

AGE_PALETTE = {
    '18-25': '#F87171', '26-35': '#FBBF24', '36-45': '#34D399',
    '46-55': '#60A5FA', '56-65': '#A78BFA', '65+':   '#64748B',
}
AGE_ORDER = ['18-25', '26-35', '36-45', '46-55', '56-65', '65+']

CAT_COLORS = {
    'Attrition':    '#F87171',
    'Balance':      '#60A5FA',
    'Interchange':  '#FBBF24',
    'Reg E':        '#34D399',
    'Payroll':      '#A78BFA',
    'Relationship': '#38BDF8',
    'Segmentation': '#818CF8',
    'Retention':    '#FB923C',
    'Engagement':   '#2DD4BF',
}

# -- Notebook-synced palettes (dark-adapted from 01_general_theme) --
BRACKET_PALETTE = [
    '#A8DADC', '#60A5FA', '#2DD4BF', '#FBBF24',
    '#FB923C', '#F87171', '#EF4444', '#A78BFA',
]
BRACKET_LABELS = ['< $1', '$1-5', '$5-10', '$10-25', '$25-50', '$50-100', '$100-500', '$500+']

ACCT_AGE_PALETTE = {
    '1-90d': '#F87171', '91-180d': '#FBBF24', '181-365d': '#FB923C',
    '1-2yr': '#34D399', '2-3yr': '#60A5FA', '3-5yr': '#818CF8',
    '5-10yr': '#A78BFA', '10-20yr': '#94A3B8', '20yr+': '#2DD4BF',
}
ACCT_AGE_ORDER = ['1-90d', '91-180d', '181-365d', '1-2yr', '2-3yr',
                  '3-5yr', '5-10yr', '10-20yr', '20yr+']

SPEND_TIER_PALETTE = {
    'Very High': '#F87171', 'High': '#FBBF24', 'Medium': '#60A5FA', 'Low': '#94A3B8',
}
SPEND_TIER_ORDER = ['Very High', 'High', 'Medium', 'Low']

SWIPE_PALETTE = {
    'Very High': '#F87171', 'High': '#FBBF24', 'Medium': '#34D399',
    'Low': '#60A5FA', 'Inactive': '#94A3B8',
}
SWIPE_ORDER = ['Very High', 'High', 'Medium', 'Low', 'Inactive']

CATEGORY_PALETTE = {
    'Big Nationals': '#F87171', 'Top 25 Fed District': '#EF4444',
    'Credit Unions': '#34D399', 'Local Banks': '#818CF8',
    'Digital Banks': '#FBBF24', 'Custom': '#FB923C',
    'Wallets': '#94A3B8', 'P2p': '#2DD4BF', 'Bnpl': '#F97316',
}
CATEGORY_ORDER = ['Big Nationals', 'Top 25 Fed District', 'Credit Unions',
                  'Local Banks', 'Digital Banks', 'Custom', 'Wallets', 'P2p', 'Bnpl']

# -- Export deck section structure --
SECTIONS = {
    'Story Arcs': [
        'Portfolio Illusions', 'Where the Money Goes', 'The Loyalty Myth',
        'The Revenue You\'re Missing', 'The Attrition Cascade', 'Deepening or Decline',
    ],
    'Operations': ['Branch Performance', 'Campaign Effectiveness'],
    'Detailed Analysis': [
        'Portfolio Overview', 'Merchant Analysis', 'MCC Categories',
        'Business Accounts', 'Personal Accounts', 'Competition',
        'Financial Services', 'ICS Acquisition', 'Campaign Analysis',
        'Branch Analysis', 'Transaction Type', 'Product Mix',
        'Attrition Risk', 'Balance Analysis', 'Interchange',
        'Reg E & Overdraft', 'Payroll & PFI', 'Relationship Depth',
        'Segment Evolution', 'Retention & Churn', 'Engagement Migration',
    ],
}

ARC_METADATA = {
    'portfolio_illusions': {
        'title': 'Portfolio Illusions',
        'subtitle': 'Portfolio health, business vs personal, product mix concentration',
        'objection': '"We\'re doing fine -- the portfolio is healthy."',
        'reality': 'Power users carry the portfolio. 34.8% are single-product members with 3x churn risk. Business accounts are undermonetized.',
        'headline': ('Single-Product Members', '34.8%', 'with 18.5% churn risk -- highest attrition segment'),
        'headline_severity': 'danger',
        'cross_refs': [('Single-product members are 3x more likely to attrite', 'The Attrition Cascade')],
        'impacts': [
            {'label': 'Relationship Revenue Lift', 'value': '$18M', 'timeframe': 'Annual', 'color': '#34D399'},
            {'label': 'Cross-Sell Targets', 'value': '11,560', 'timeframe': 'Accounts', 'color': '#60A5FA'},
            {'label': 'Business Monetization Gap', 'value': '2.7x', 'timeframe': 'vs Personal', 'color': '#FBBF24'},
        ],
        'findings': [
            {'category': 'Single Product', 'finding': '34.8% are single-product members with 18.5% churn risk -- highest priority for cross-sell', 'priority': 'High'},
            {'category': 'Revenue Curve', 'finding': 'Each additional product adds ~$340/mo avg spend and reduces churn by 6pp', 'priority': 'High'},
            {'category': 'Business Gap', 'finding': 'Business accounts are 14.5% of portfolio but spend 2.7x personal -- undermonetized', 'priority': 'High'},
            {'category': 'Product Dominance', 'finding': 'Top product = 68% of transactions; others are neglected', 'priority': 'Medium'},
        ],
    },
    'spending_patterns': {
        'title': 'Where the Money Goes',
        'subtitle': 'Merchant concentration, MCC categories, transaction types',
        'objection': '"Our transaction volume is diversified."',
        'reality': 'Top 5 merchants = 38% of volume. Median members use only 1-2 MCC categories. Single-category users are 3x churn risk.',
        'headline': ('Top 5 Merchant Share', '38%', 'of all transaction volume -- dangerous concentration'),
        'headline_severity': 'warning',
        'cross_refs': [('Merchant concentration amplifies attrition risk', 'The Attrition Cascade')],
        'impacts': [
            {'label': 'Concentration Risk', 'value': '38%', 'timeframe': 'Top 5 Share', 'color': '#FBBF24'},
            {'label': 'Single-Category Churn', 'value': '3x', 'timeframe': 'vs Multi-Category', 'color': '#F87171'},
            {'label': 'PIN->SIG Opportunity', 'value': '$420K', 'timeframe': 'Annual', 'color': '#34D399'},
        ],
        'findings': [
            {'category': 'Merchant Concentration', 'finding': 'Top 5 merchants = 38% of volume -- single merchant loss would materially impact portfolio', 'priority': 'High'},
            {'category': 'Category Diversity', 'finding': 'Median members use 1-2 MCC categories; single-category users have 3x churn risk', 'priority': 'High'},
            {'category': 'Signature Shift', 'finding': 'PIN transactions dominate small-ticket; shifting to SIG adds $420K annual interchange', 'priority': 'Medium'},
        ],
    },
    'loyalty_myth': {
        'title': 'The Loyalty Myth',
        'subtitle': 'Competitor penetration, fintech leakage, acquisition channel quality',
        'objection': '"Members are loyal."',
        'reality': '55.5% have competitor card activity. High-balance members send 30%+ of card spend elsewhere. Fintech leakage is growing.',
        'headline': ('Competitor Penetration', '55.5%', 'of members use a competitor card'),
        'headline_severity': 'danger',
        'cross_refs': [
            ('Accounts with 2+ competitors are 3.8x more likely to attrite', 'The Attrition Cascade'),
            ('Competitor activity correlates with deposit flight', 'The Revenue You\'re Missing'),
        ],
        'impacts': [
            {'label': 'Recoverable Spend', 'value': '$61M', 'timeframe': 'Annual', 'color': '#34D399'},
            {'label': 'FinTech Leakage', 'value': '$15M', 'timeframe': 'Annual', 'color': '#F87171'},
            {'label': 'ICS Activation Gap', 'value': '2,480', 'timeframe': 'Accounts', 'color': '#60A5FA'},
        ],
        'findings': [
            {'category': 'Competitor Penetration', 'finding': '55.5% of accounts show competitor activity -- "loyalty" is a myth', 'priority': 'High'},
            {'category': 'High-Balance Flight', 'finding': 'High-balance members ($10K+) send 30%+ of card spend to competitors', 'priority': 'High'},
            {'category': 'Fintech Threat', 'finding': 'Digital-first competitors (Venmo, Cash App, PayPal) growing fastest among 18-35', 'priority': 'High'},
            {'category': 'Channel Quality', 'finding': 'ICS referral channel produces 2.3x more engaged members than direct mail', 'priority': 'Medium'},
        ],
    },
    'revenue_missing': {
        'title': 'The Revenue You\'re Missing',
        'subtitle': 'Interchange optimization, Reg E & overdraft, payroll capture',
        'objection': '"Revenue is locked in by the networks. Overdraft is stable. Payroll is just another service."',
        'reality': '$420K interchange sitting on the table. OD opt-in declining. Only 28.1% payroll detected vs 50% industry.',
        'headline': ('Payroll Detection', '28.1%', 'vs 50% industry -- each payroll = $2,480 deposit lift'),
        'headline_severity': 'warning',
        'cross_refs': [('Payroll members have 40% lower churn than non-payroll', 'The Attrition Cascade')],
        'impacts': [
            {'label': 'PIN->SIG Shift', 'value': '$420K', 'timeframe': 'Annual', 'color': '#34D399'},
            {'label': 'Reg E Revenue Risk', 'value': '$1.1M', 'timeframe': 'If Opt-In -10%', 'color': '#F87171'},
            {'label': 'Payroll Gap', 'value': '22pp', 'timeframe': 'vs Industry', 'color': '#FBBF24'},
        ],
        'findings': [
            {'category': 'Interchange', 'finding': 'Shifting 25% of PIN to SIG = +$420K annual interchange revenue', 'priority': 'High'},
            {'category': 'Reg E Erosion', 'finding': 'Opt-in rate declining 0.3%/month -- protect this $1.1M revenue stream', 'priority': 'High'},
            {'category': 'Payroll Capture', 'finding': '28.1% payroll detection vs 50% industry -- each capture adds $2,480 in deposits', 'priority': 'High'},
            {'category': 'PFI Scoring', 'finding': 'Only 38% are Primary FI -- upgrade path from Secondary adds $3,200 avg balance', 'priority': 'Medium'},
        ],
    },
    'attrition_cascade': {
        'title': 'The Attrition Cascade',
        'subtitle': 'Risk scoring, balance flight, churn cost quantification',
        'objection': '"Attrition is just part of the business."',
        'reality': '18.3% of accounts are declining or at-risk. $12M annual spend lost from closed accounts. Dormant accounts cost $2.1M in residual activity.',
        'headline': ('Annual Revenue Lost', '$12M', 'from closed accounts alone -- retention investment pays for itself'),
        'headline_severity': 'danger',
        'cross_refs': [('Competitor presence is the #1 predictor of attrition', 'The Loyalty Myth')],
        'impacts': [
            {'label': 'Closed Account Loss', 'value': '$12M', 'timeframe': 'Annual', 'color': '#F87171'},
            {'label': 'At-Risk Pipeline', 'value': '7,750', 'timeframe': 'Accounts', 'color': '#FBBF24'},
            {'label': 'Dormant Residual', 'value': '$2.1M', 'timeframe': 'Recoverable', 'color': '#34D399'},
        ],
        'findings': [
            {'category': 'Churn Cost', 'finding': '$12M annual spend lost from closed accounts -- retention investment justified', 'priority': 'High'},
            {'category': 'Dormant Pipeline', 'finding': '3,650 dormant accounts with $2.1M residual activity -- reactivation window closing', 'priority': 'High'},
            {'category': 'PFI Correlation', 'finding': 'Incidental PFI tier has 8.2% churn vs 1.2% for Primary -- deepen relationships first', 'priority': 'High'},
            {'category': 'Deposit Flight', 'finding': 'High-balance accounts with competitor activity show 3x faster balance decline', 'priority': 'High'},
            {'category': 'Early Warning', 'finding': 'Accounts with 2+ risk signals close within 6 months 40% of the time', 'priority': 'Medium'},
        ],
    },
    'deepening_decline': {
        'title': 'Deepening or Decline',
        'subtitle': 'Relationship depth, segment migration, engagement momentum',
        'objection': '"Engagement tiers are stable. Members hold the products they need."',
        'reality': 'More members degrading than upgrading. 34.8% single-product with 3x churn. Only 4% of dormant recover.',
        'headline': ('Net Migration', '-8.7%', 'more members downgrading than upgrading each quarter'),
        'headline_severity': 'warning',
        'cross_refs': [('Degrading members show competitor activity 2x more often', 'The Loyalty Myth')],
        'impacts': [
            {'label': 'Cross-Sell Revenue', 'value': '$18M', 'timeframe': 'Annual Lift', 'color': '#34D399'},
            {'label': 'Dormant Recovery', 'value': '4%', 'timeframe': 'Recovery Rate', 'color': '#F87171'},
            {'label': 'Campaign Multiplier', 'value': '2x', 'timeframe': 'Responder Upgrade Rate', 'color': '#60A5FA'},
        ],
        'findings': [
            {'category': 'Net Migration', 'finding': 'Upgrade:degrade ratio 1.4:1 -- positive but fragile; campaigns drive most upgrades', 'priority': 'High'},
            {'category': 'Dormant Stickiness', 'finding': '84% of Dormant remain Dormant -- need aggressive reactivation before it\'s too late', 'priority': 'High'},
            {'category': 'Single Product', 'finding': '34.8% single-product with 18.5% churn -- deepening from 1->2 products is highest-leverage move', 'priority': 'High'},
            {'category': 'Campaign Impact', 'finding': 'Responders upgrade at 2x the rate of non-responders -- campaigns drive real tier changes', 'priority': 'Medium'},
        ],
    },
}
