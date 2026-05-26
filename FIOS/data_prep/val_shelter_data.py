def prepare_shelter_data(raw_shelter_df):
    """cleans and validates raw shelter data"""

    df = raw_shelter_df.copy()

    year_col = 'year' if 'year' in df.columns else 'Year'
    animal_type_col = 'animal_type' if 'animal_type' in df.columns else 'Animal Type'
    intake_type_col = 'intake_type' if 'intake_type' in df.columns else 'Intake Type'
    animal_id_col = 'animal_id' if 'animal_id' in df.columns else 'Animal ID'

    df['year'] = df[year_col].astype(int)
    df['animal_type'] = df[animal_type_col].astype(str).str.strip().str.capitalize()
    df['intake_type'] = df[intake_type_col].astype(str).str.strip().str.capitalize()
    df['animal_id'] = df[animal_id_col]

    df = df[df['animal_type'].notna() & (df['animal_type'] != 'None') & (df['animal_type'] != '')]
    df = df[df['intake_type'].notna() & (df['intake_type'] != 'None') & (df['intake_type'] != '')]
    df = df.dropna(subset=['animal_id'])

    transformed_df = df[['year', 'animal_type', 'intake_type', 'animal_id']].copy()

    return transformed_df

def generate_shelter_metrics(transformed_df):
    """calculates total intakes by year/intake type"""

    aggregated_df = transformed_df.groupby(['year', 'intake_type']).agg(
        total_intakes=('animal_id', 'count')
    ).reset_index()

    return aggregated_df

def merge_shelter_data(aggregated_df):
    """calculates total intakes by year"""

    aggregated_df['feature_name'] = (
            aggregated_df['intake_type'].str.lower().str.replace(' ', '_') +
            '_count'
    )

    merged_df = aggregated_df.pivot(
        index='year',
        columns='feature_name',
        values='total_intakes'
    ).fillna(0)

    merged_df['total_animals_count'] = merged_df.sum(axis=1)
    merged_df = merged_df.reset_index()

    cols = ['year', 'total_animals_count'] + [c for c in merged_df.columns if c not in ['year', 'total_animals_count']]

    return merged_df[cols]