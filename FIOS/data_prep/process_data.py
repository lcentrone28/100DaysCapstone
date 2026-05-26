import pandas as pd
import os
from data_prep.data_loader import load_irs_data, load_shelter_data
from data_prep.val_irs_data import prepare_irs_for_index, generate_poverty_index, prepare_irs_overall, generate_overall_poverty_index
from data_prep.val_shelter_data import prepare_shelter_data, generate_shelter_metrics, merge_shelter_data

def process_irs_data():
    print("loading IRS data...\n")
    raw_irs_df = load_irs_data()

    prepped_irs_by_zip = prepare_irs_for_index(raw_irs_df)
    poverty_by_zip_df = generate_poverty_index(prepped_irs_by_zip)

    prepped_irs_overall = prepare_irs_overall(raw_irs_df)
    poverty_overall_df = generate_overall_poverty_index(prepped_irs_overall)

    return poverty_by_zip_df, poverty_overall_df

def process_shelter_data():
    print("loading shelter data...\n")
    raw_shelter_df = load_shelter_data()

    prepped_shelter = prepare_shelter_data(raw_shelter_df)
    shelter_metrics = generate_shelter_metrics(prepped_shelter)
    overall_shelter_df = merge_shelter_data(shelter_metrics)

    return overall_shelter_df

def merge_zip_dataset(poverty_by_zip_df, overall_shelter_df):
    """combines IRS zip data and shelter data"""

    merged_df = pd.merge(poverty_by_zip_df, overall_shelter_df, on='year', how='inner')
    merged_df = merged_df.sort_values(['year', 'zip_code']).reset_index(drop=True)

    return merged_df

def merge_overall_dataset(poverty_overall_df, overall_shelter_df):
    """combines IRS overall data and shelter data"""

    merged_df = pd.merge(poverty_overall_df, overall_shelter_df, on='year', how='inner')
    merged_df = merged_df.sort_values('year').reset_index(drop=True)

    return merged_df

def merge_data(poverty_by_zip_df, poverty_overall_df, overall_shelter_df):
    final_zip_df = merge_zip_dataset(poverty_by_zip_df, overall_shelter_df)
    final_overall_df = merge_overall_dataset(poverty_overall_df, overall_shelter_df)

    output_dir = os.path.join("data_prep", "merged_data")
    os.makedirs(output_dir, exist_ok=True)

    final_zip_df.to_csv(os.path.join(output_dir, "zip_trends.csv"), index=False)
    final_overall_df.to_csv(os.path.join(output_dir, "overall_trends.csv"), index=False)
    print("merged data")

def process_data():
    poverty_by_zip_df, poverty_overall_df = process_irs_data()
    overall_shelter_df = process_shelter_data()
    merge_data(poverty_by_zip_df, poverty_overall_df, overall_shelter_df)