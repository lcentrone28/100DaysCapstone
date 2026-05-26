import os
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

GREEN = "#1a9850"
YELLOW = "#fee08b"
ORANGE = "#f46d43"
RED = "#e31a1c"
DARKRED = "#7f0000"

GRAYSCALE_PALETTE = [
    "rgba(40, 40, 40, 0.9)",
    "rgba(100, 100, 100, 0.9)",
    "rgba(160, 160, 160, 0.9)",
    "rgba(70, 70, 70, 0.9)"
]

OVERALL_PATH = os.path.join("data_prep", "merged_data", "overall_trends.csv")
ZIP_PATH = os.path.join("data_prep", "merged_data", "zip_trends.csv")

def verify_data_assets_exist() -> bool:
    return os.path.exists(OVERALL_PATH) and os.path.exists(ZIP_PATH)

def handle_missing_assets():
    st.error("Data files missing: Uncomment process_data() in main.py and run it once first.")
    st.stop()

@st.cache_data
def read_raw_csv_data():
    df_overall = pd.read_csv(OVERALL_PATH)
    df_zip = pd.read_csv(ZIP_PATH)
    return df_overall, df_zip

def load_verify_dataset():
    if not verify_data_assets_exist():
        handle_missing_assets()
    return read_raw_csv_data()

def extract_dataframe_metrics(df_overall: pd.DataFrame, df_zip: pd.DataFrame = None) -> dict:
    """extracts years, zip codes, and intake data; returns a dict"""

    df_zip_source = df_zip if df_zip is not None else df_overall

    unique_years = sorted(list(df_overall['year'].unique()))
    unique_zips = sorted(list(df_zip_source['zip_code'].astype(str).unique()))
    intake_cols = [
        c for c in df_overall.columns
        if c.endswith('_count') and c != 'total_animals_count'
    ]

    return {
        "years": unique_years,
        "zips": unique_zips,
        "intake_columns": intake_cols
    }

def ui_render_year_slider(all_years: list):
    return st.sidebar.slider(
        "Year Range:",
        min_value=int(min(all_years)),
        max_value=int(max(all_years)),
        value=(int(min(all_years)), int(max(all_years))),
        label_visibility="collapsed"
    )

def ui_render_irs_radio() -> str:
    return st.sidebar.radio(
        "IRS Poverty Index:",
        options=[
            "Overall",
            "All Zips",
            "By Specific Zip",
            "By Selected Zips"
        ],
        label_visibility="collapsed"
    )

def ui_render_zip_text_search(default_zip: str) -> str:
    return st.sidebar.text_input("Zip Code:", value=default_zip).strip()

def ui_render_zip_multiselect(options_zips: list) -> list:
    return st.sidebar.multiselect(
        "Zip Codes:",
        options=options_zips,
        default=options_zips[:3]
    )

def ui_render_details_checkbox() -> bool:
    return st.sidebar.checkbox("Show Breakdown", value=False)

def ui_render_intake_multiselect(intake_types: list) -> list:
    label_mapping = {
        "abandoned_count": "Abandoned",
        "euthanasia_count": "Euthanasia",
        "owner_surrender_count": "Owner Surrender",
        "public_assist_count": "Public Assist"
    }

    ui_labels = [label_mapping.get(t, t.replace('_count', '').title()) for t in intake_types]

    chosen_labels = st.sidebar.multiselect(
        "Intake Types:",
        options=ui_labels,
        default=ui_labels
    )

    reverse_mapping = {v: k for k, v in label_mapping.items()}
    return [reverse_mapping.get(lbl, f"{lbl.lower()}_count") for lbl in chosen_labels]

def render_sidebar_controls(all_years, unique_zips, intake_types) -> dict:
    st.sidebar.header("Dashboard Controls")

    st.sidebar.subheader("Year Range:")
    year_range = ui_render_year_slider(all_years)

    st.sidebar.subheader("IRS Poverty Index")
    irs_mode = ui_render_irs_radio()

    search_query = ""
    multiselect_zips = []
    if irs_mode == "By Specific Zip":
        search_query = ui_render_zip_text_search(unique_zips[0])
    elif irs_mode == "By Selected Zips":
        multiselect_zips = ui_render_zip_multiselect(unique_zips)

    st.sidebar.subheader("Shelter Intake")
    show_details = ui_render_details_checkbox()

    selected_intakes = []
    if show_details:
        selected_intakes = ui_render_intake_multiselect(intake_types)

    return {
        "year_range": year_range,
        "irs_mode": irs_mode,
        "search_query": search_query,
        "multiselect_zips": multiselect_zips,
        "show_details": show_details,
        "selected_intakes": selected_intakes
    }

def determine_target_zips(irs_mode: str, search_query: str, multiselect_zips: list, unique_zips: list) -> list:
    if irs_mode == "All Zips":
        return unique_zips
    if irs_mode == "By Specific Zip":
        if search_query in unique_zips:
            return [search_query]
        st.sidebar.warning("Invalid Zip Code")
        return []
    if irs_mode == "By Selected Zips":
        return multiselect_zips
    return []

def filter_dataframe_by_years(df: pd.DataFrame, year_range: tuple) -> pd.DataFrame:
    years_to_keep = list(range(year_range[0], year_range[1] + 1))
    return df[df['year'].isin(years_to_keep)].sort_values('year')

def filter_dataframe_by_zips(df_zip: pd.DataFrame, target_zips: list) -> pd.DataFrame:
    return df_zip[df_zip['zip_code'].astype(str).isin(target_zips)].copy()

def get_population_bracket_color(avg_pop: float) -> str:
    if avg_pop < 5000:
        return GREEN
    elif avg_pop < 15000:
        return YELLOW
    elif avg_pop < 25000:
        return ORANGE
    elif avg_pop < 50000:
        return RED
    return DARKRED

def compute_sorted_intakes(df_overall: pd.DataFrame, selected_intakes: list) -> list:
    intake_sums = df_overall[selected_intakes].sum().sort_values(ascending=False)
    return intake_sums.index.tolist()

def create_baseline_bar_trace(df_overall: pd.DataFrame) -> go.Bar:
    return go.Bar(
        x=df_overall['year'],
        y=df_overall['total_animals_count'],
        name="Total Intakes Baseline",
        marker_color="rgba(220, 220, 220, 0.4)",
        yaxis="y1",
        offsetgroup=1
    )

def create_stacked_bar_trace(df_overall: pd.DataFrame, intake_column: str, execution_index: int) -> go.Bar:
    color_assigned = GRAYSCALE_PALETTE[execution_index % len(GRAYSCALE_PALETTE)]
    clean_name = intake_column.replace('_count', '').replace('_', ' ').title()

    return go.Bar(
        x=df_overall['year'],
        y=df_overall[intake_column],
        name=clean_name,  # Updated here
        marker_color=color_assigned,
        yaxis="y1",
        offsetgroup=1
    )

def create_citywide_line_trace(df_overall: pd.DataFrame) -> go.Scatter:
    return go.Scatter(
        x=df_overall['year'],
        y=df_overall['poverty_index'],
        name="Overall Poverty Index",
        line=dict(color="darkred", width=5, dash="solid"),
        yaxis="y2",
        mode="lines+markers"
    )

def create_zip_line_trace(zip_data: pd.DataFrame, zip_val: str, color_hex: str, show_legend: bool) -> go.Scatter:
    return go.Scatter(
        x=zip_data['year'],
        y=zip_data['poverty_index'],
        name=f"Zip {zip_val}",
        mode="lines+markers",
        yaxis="y2",
        opacity=0.50,
        line=dict(width=3.5, color=color_hex),
        marker=dict(size=6, color=color_hex),
        hoverinfo="text",
        text=[f"Zip Code: {zip_val}<br>Year: {y}<br>Poverty Index: {p:.2f}<br>Total Returns: {int(r)}"
              for y, p, r in zip(zip_data['year'], zip_data['poverty_index'], zip_data['num_returns_total'])],
        showlegend=show_legend
    )

def create_colorbar_anchor_trace() -> go.Scatter:
    return go.Scatter(
        x=[None], y=[None],
        mode='markers',
        yaxis='y2',
        marker=dict(
            colorscale=[
                [0.0, GREEN],
                [0.06, YELLOW],
                [0.27, ORANGE],
                [0.48, RED],
                [1.0, DARKRED]
            ],
            cmin=2000,
            cmax=50000,
            colorbar=dict(
                title=dict(text="Population Size<br>(Total Returns)", font=dict(color="white")),
                tickfont=dict(color="white"),
                thickness=15,
                x=1.12,
                yanchor="middle",
                y=0.5,
                tickmode="array",
                tickvals=[2000, 5000, 10000, 15000, 25000, 50000],
                ticktext=["2k", "5k", "10k", "15k", "25k", "50k"]
            ),
            showscale=True
        ),
        hoverinfo='none',
        showlegend=False
    )

def build_shelter_layer(fig: go.Figure, df_overall: pd.DataFrame, controls: dict):
    if df_overall.empty:
        return

    if not controls["show_details"]:
        fig.add_trace(create_baseline_bar_trace(df_overall))
    elif controls["selected_intakes"]:
        sorted_intakes = compute_sorted_intakes(df_overall, controls["selected_intakes"])
        for idx, intake in enumerate(sorted_intakes):
            fig.add_trace(create_stacked_bar_trace(df_overall, intake, idx))

def build_poverty_layer(fig: go.Figure, df_overall: pd.DataFrame, df_zip: pd.DataFrame, controls: dict, unique_zips: list):
    irs_mode = controls["irs_mode"]

    if irs_mode == "Overall":
        if not df_overall.empty:
            fig.add_trace(create_citywide_line_trace(df_overall))
        return

    target_zips = determine_target_zips(irs_mode, controls["search_query"], controls["multiselect_zips"], unique_zips)
    if not target_zips:
        return

    filtered_zip_df = filter_dataframe_by_zips(df_zip, target_zips)
    if filtered_zip_df.empty:
        return

    for zip_val in filtered_zip_df['zip_code'].unique():
        zip_data = filtered_zip_df[filtered_zip_df['zip_code'] == zip_val].sort_values('year')
        avg_pop = float(zip_data['num_returns_total'].mean())
        color_hex = get_population_bracket_color(avg_pop)
        show_legend = (irs_mode != "All Zips")

        fig.add_trace(create_zip_line_trace(zip_data, zip_val, color_hex, show_legend))

    fig.add_trace(create_colorbar_anchor_trace())

def apply_master_canvas_layout(fig: go.Figure, year_range: tuple):
    years_window = list(range(year_range[0], year_range[1] + 1))
    fig.update_layout(
        xaxis=dict(
            title=dict(text="Years", font=dict(color="white")),
            tickfont=dict(color="white"),
            tickmode="array",
            tickvals=years_window,
            gridcolor="rgba(250, 250, 250, 0.1)"
        ),
        yaxis=dict(
            title=dict(text="Shelter Intake", font=dict(color="white", size=13)),
            tickfont=dict(color="white"),
            gridcolor="rgba(250, 250, 250, 0.1)",
            side="right"
        ),
        yaxis2=dict(
            title=dict(text="Poverty Index", font=dict(color="white", size=13)),
            tickfont=dict(color="white"),
            anchor="x",
            overlaying="y",
            side="left",
            showgrid=False
        ),
        barmode="stack",
        legend=dict(
            font=dict(color="white"),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=680,
        margin=dict(l=40, r=120, t=80, b=40),
        hovermode="closest"
    )

def run_dashboard():
    st.set_page_config(page_title="Financial Impact on Shelters", layout="wide")

    st.html(
        """
        <style>
            /* shrink main padding */
            .block-container {
                padding-top: 3.5rem !important;
                padding-bottom: 0rem !important;
            }
            /* remove sidebar top padding */
            [data-testid="stSidebarUserContent"] {
                padding-top: 0rem !important;
            }
        </style>
        """
    )

    st.header("Financial Impact on Shelters")

    df_overall, df_zip = load_verify_dataset()

    metrics = extract_dataframe_metrics(df_overall, df_zip)
    all_years = metrics["years"]
    unique_zips = metrics["zips"]
    intake_types = metrics["intake_columns"]

    controls = render_sidebar_controls(all_years, unique_zips, intake_types)

    filtered_overall = filter_dataframe_by_years(df_overall, controls["year_range"])
    filtered_zip = filter_dataframe_by_years(df_zip, controls["year_range"])

    fig = go.Figure()
    build_shelter_layer(fig, filtered_overall, controls)
    build_poverty_layer(fig, filtered_overall, filtered_zip, controls, unique_zips)
    apply_master_canvas_layout(fig, controls["year_range"])

    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    run_dashboard()