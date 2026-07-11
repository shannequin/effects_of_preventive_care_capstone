import statsmodels.formula.api as smf
import streamlit as st

from config.analysis_config import ANALYSIS_CONFIG
from utils.plotting_utils import plot_odds_ratio


CONN = st.connection("postgresql", type="sql")

def analysis(selected_care: str, selected_analysis: str) -> None:
    """
    Perform analysis on the relationship between given care and given indicator.
    """
    # Format query based on the selected care and analysis
    screening_list = ANALYSIS_CONFIG[selected_care]['Screenings']
    indicator = ANALYSIS_CONFIG[selected_care]['Analysis'][selected_analysis]['indicator']

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

    # Format the formula for logistic regression, using the base category if specified in the config
    base_category = ANALYSIS_CONFIG[selected_care]['Analysis'][selected_analysis].get('base_category')
    formula = f'any_screenings ~ C({indicator}, Treatment(reference=\'{base_category}\'))'

    # Fit a classification logistic regression model
    model = smf.logit(
        formula=formula,
        data=df
    ).fit()

    # Plot the odds ratio
    plot_df = plot_odds_ratio(model, selected_care, selected_analysis)

    st.dataframe(
            plot_df[["label", "odds_ratio", "p_value"]]
            .sort_values("odds_ratio", ascending=False),
            hide_index=True,
        )