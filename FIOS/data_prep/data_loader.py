import pandas as pd
import requests
from data_prep.shelter_data import SHELTER_APP_TOKEN, API_ENDPOINT

def load_irs_data():
    years = range(11, 23)
    all_years = []

    column_mapping = {
        'Size of adjusted gross income': 'income_bracket',
        'Number of returns': 'num_returns',
        'Adjusted gross income (AGI)': 'agi',
        'Salaries and wages in AGI': 'salaries_wages',
        'Unemployment compensation': 'unemployment_comp',
        'Earned income credit': 'earned_income_credit',
    }

    for year in years:
        ext = ".xls" if year <= 16 else ".xlsx"
        filename = f"data_prep/irs_data/{year:02d}zp44tx{ext}"

        header = pd.read_excel(filename, header=None, skiprows=3, nrows=1).iloc[0]

        found_cols = {0: 'zip_code'}

        for i, val in enumerate(header):
            if isinstance(val, str):
                for target, clean_name in column_mapping.items():
                    if target.lower() in val.lower() and 'excess' not in val.lower():
                        if clean_name not in found_cols.values():
                            found_cols[i] = clean_name
                        break

        col_indices = list(found_cols.keys())
        df = pd.read_excel(filename, header=None, skiprows=6, usecols=col_indices)

        df.columns = [found_cols[i] for i in col_indices]

        df = df[df['zip_code'].astype(str).str.startswith(('786', '787'))]

        df['year'] = 2000 + year
        all_years.append(df)

    return pd.concat(all_years, ignore_index=True)

def load_shelter_data():
    all_records = []
    limit = 1000
    offset = 0

    while True:
        params = {
            "$$app_token": SHELTER_APP_TOKEN,
            "$limit": limit,
            "$offset": offset,
            "$order": "datetime"
        }

        response = requests.get(API_ENDPOINT, params=params)
        records = response.json()

        if not records:
            break

        all_records.extend(records)
        offset += limit

    df = pd.DataFrame(all_records)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['year'] = df['datetime'].dt.year

    return df