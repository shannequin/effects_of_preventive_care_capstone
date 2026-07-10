import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import streamlit as st
import textwrap


CONN = st.connection("postgresql", type="sql")

def plot_odds_ratio(model, path: str) -> None:
    """
    Create and save an error bar plot of odds ratios.
    """
    # Create a dataframe for plotting
    plot_df = pd.DataFrame({
        'term': model.params.index,
        'coef': model.params.values,
        'ci_lower': model.conf_int()[0].values,
        'ci_upper': model.conf_int()[1].values,
        'p_value': model.pvalues.values
    })
    print(plot_df)

    # Remove the intercept row
    plot_df = plot_df[plot_df['term'] != 'Intercept'].copy()

    # Convert log odds to odds ratios for interpretability
    plot_df['odds_ratio'] = np.exp(plot_df['coef'])
    plot_df['or_ci_lower'] = np.exp(plot_df['ci_lower'])
    plot_df['or_ci_upper'] = np.exp(plot_df['ci_upper'])

    # Clean long statsmodels categorical labels
    plot_df['label'] = (
        plot_df['term']
        .str.replace(r'C\(primins2\)\[T\.', '', regex=True)
        .str.replace(r'\]$', '', regex=True)
    )

    # Wrap labels
    plot_df['label'] = plot_df['label'].apply(lambda x: '\n'.join(textwrap.wrap(x, width=45)))

    # Sort by odds ratio
    plot_df = plot_df.sort_values('odds_ratio')

    # Set the figure size
    plt.figure(figsize=(10, 8))

    # Create the figure
    plt.errorbar(
        x=plot_df['odds_ratio'],
        y=plot_df['label'],
        xerr=[
            plot_df['odds_ratio'] - plot_df['or_ci_lower'],
            plot_df['or_ci_upper'] - plot_df['odds_ratio']
        ],
        fmt="o",
        capsize=4
    )

    # Set odds ratio 1 indicator
    plt.axvline(1, linestyle="--", linewidth=1)
    plt.xlabel("Odds Ratio")
    fig = plt.gcf()

    # Save fig as png
    fig.savefig(f'src/figures/{path}.png', bbox_inches='tight')

def colorectal_insurance_analysis() -> tuple[pd.DataFrame, 'model']:
    """
    Perform analysis on the relationship between primary insurance type and preventive care for colon cancer.
    """
    # Fetch data for all colorectal cancer screenings and insurance types
    query = """SELECT
                hadsigm4,
                colncncr,
                vircolo1,
                smalstol,
                stooldn2,
                primins2
            FROM staging.behavioral_risk_factor_surveillance_system
            WHERE primins2 IS NOT NULL
            AND (
                hadsigm4 IS NOT NULL
                OR colncncr IS NOT NULL
                OR vircolo1 IS NOT NULL
                OR smalstol IS NOT NULL
                OR stooldn2 IS NOT NULL
            );"""

    # Query the database
    df = CONN.query(sql=query)

    # List of screenings
    screening_list = ["hadsigm4", "colncncr", "vircolo1", "smalstol", "stooldn2"]

    # Create column for any screenings
    df['any_screenings'] = (
        df[screening_list]
        .eq('Yes')
        .any(axis=1)
        .astype(int)
    )

    # Fit a classification logistic regression model
    model = smf.logit(
        formula='any_screenings ~ C(primins2)',
        data=df
    ).fit()

    # Plot the odds ratio
    plot_odds_ratio(model=model, path='colon_odds_ratios')

    return df, model