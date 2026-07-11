import pandas as pd
import statsmodels.formula.api as smf
import streamlit as st

from config.analysis_config import ANALYSIS_CONFIG
from utils.plotting_utils import plot_odds_ratio


CONN = st.connection("postgresql", type="sql")

def analysis(care: str, indicator: str) -> tuple[pd.DataFrame, str]:
    """
    Perform analysis on the relationship between given care and given indicator.
    """
    screening_list = ANALYSIS_CONFIG[care]['Screenings']

    query = f"""SELECT
                    {', '.join(screening_list)},
                    {indicator}
                FROM staging.behavioral_risk_factor_surveillance_system
                WHERE {indicator} IS NOT NULL
                AND (
                    {' OR '.join([f"{screening} IS NOT NULL" for screening in screening_list])}
                );"""

    # Query the database
    df = CONN.query(sql=query)

    # Create column for any screenings
    df['any_screenings'] = (
        df[screening_list]
        .eq('Yes')
        .any(axis=1)
        .astype(int)
    )

    # Fit a classification logistic regression model
    model = smf.logit(
        formula=f'any_screenings ~ C({indicator})',
        data=df
    ).fit()

    # Plot the odds ratio
    plot_df, plot_path = plot_odds_ratio(model=model, indicator=indicator)

    return plot_df, plot_path