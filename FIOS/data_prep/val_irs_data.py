import pandas as pd

def prepare_irs_for_index(raw_irs_df):
    """transforms raw IRS data into a single row per zip/year"""

    totals_df = raw_irs_df[raw_irs_df['income_bracket'].isna()].copy()
    brackets_df = raw_irs_df[raw_irs_df['income_bracket'].notna()].copy()
    low_income_df = brackets_df[brackets_df['income_bracket'] == '$1 under $25,000'].copy()

    totals_df = totals_df.rename(columns={
        'num_returns': 'num_returns_total',
        'unemployment_comp': 'unemployment_returns',
        'earned_income_credit': 'earned_income_credit_returns'
    })

    low_income_df = low_income_df.rename(columns={
        'num_returns': 'low_income_returns'
    })

    prepped_df = pd.merge(
        totals_df[['year', 'zip_code', 'num_returns_total', 'unemployment_returns', 'earned_income_credit_returns']],
        low_income_df[['year', 'zip_code', 'low_income_returns']],
        on=['year', 'zip_code'],
        how='inner'
    )

    return prepped_df

def generate_poverty_index(df):
    """gauges poverty of zip codes"""

    df['eic_ratio'] = df['earned_income_credit_returns'] / df['num_returns_total']
    df['unemployment_ratio'] = df['unemployment_returns'] / df['num_returns_total']
    df['low_income_ratio'] = df['low_income_returns'] / df['num_returns_total']

    for col in ['eic_ratio', 'unemployment_ratio', 'low_income_ratio']:
        min_val = df[col].min()
        max_val = df[col].max()
        df[f'{col}_scaled'] = (df[col] - min_val) / (max_val - min_val)

    df['poverty_index'] = (
            (df['low_income_ratio_scaled'] * 0.45) +
            (df['eic_ratio_scaled'] * 0.45) +
            (df['unemployment_ratio_scaled'] * 0.10)
    )

    return df

def prepare_irs_overall(raw_irs_df):
    """transforms raw IRS data into a single row per year"""

    totals_df = raw_irs_df[raw_irs_df['income_bracket'].isna()].copy()
    brackets_df = raw_irs_df[raw_irs_df['income_bracket'].notna()].copy()
    low_income_df = brackets_df[brackets_df['income_bracket'] == '$1 under $25,000'].copy()

    totals_df = totals_df.rename(columns={
        'num_returns': 'num_returns_total',
        'unemployment_comp': 'unemployment_returns',
        'earned_income_credit': 'earned_income_credit_returns'
    })

    low_income_df = low_income_df.rename(columns={
        'num_returns': 'low_income_returns'
    })

    totals_overall = totals_df.groupby('year')[[
        'num_returns_total',
        'unemployment_returns',
        'earned_income_credit_returns'
    ]].sum().reset_index()

    low_income_overall = low_income_df.groupby('year')[['low_income_returns']].sum().reset_index()

    prepped_df = pd.merge(
        totals_overall,
        low_income_overall,
        on='year',
        how='inner'
    )

    return prepped_df


def generate_overall_poverty_index(df):
    """gauges overall poverty across all zip codes"""

    df['eic_ratio'] = df['earned_income_credit_returns'] / df['num_returns_total']
    df['unemployment_ratio'] = df['unemployment_returns'] / df['num_returns_total']
    df['low_income_ratio'] = df['low_income_returns'] / df['num_returns_total']

    for col in ['eic_ratio', 'unemployment_ratio', 'low_income_ratio']:
        min_val = df[col].min()
        max_val = df[col].max()

        if min_val == max_val:
            df[f'{col}_scaled'] = df[col]
        else:
            df[f'{col}_scaled'] = (df[col] - min_val) / (max_val - min_val)

    df['poverty_index'] = (
            (df['low_income_ratio_scaled'] * 0.45) +
            (df['eic_ratio_scaled'] * 0.45) +
            (df['unemployment_ratio_scaled'] * 0.10)
    )

    return df