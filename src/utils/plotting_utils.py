import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import textwrap


def plot_odds_ratio(model, indicator: str) -> pd.DataFrame:
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

    # Remove non statistically significant terms (p > 0.05)
    plot_df = plot_df[plot_df['p_value'] <= 0.05].copy()

    # Convert p-value to scientific notation for display
    plot_df['p_value'] = plot_df['p_value'].apply(lambda x: f"{x:.2e}")

    # Remove the intercept row
    plot_df = plot_df[plot_df['term'] != 'Intercept'].copy()

    # Convert log odds to odds ratios for interpretability
    plot_df['odds_ratio'] = np.exp(plot_df['coef'])
    plot_df['or_ci_lower'] = np.exp(plot_df['ci_lower'])
    plot_df['or_ci_upper'] = np.exp(plot_df['ci_upper'])

    # Clean long statsmodels categorical labels
    plot_df['label'] = (
        plot_df['term']
        .str.replace(rf'C\({indicator}\)\[T\.', '', regex=True)
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
        fmt='o',
        capsize=4
    )

    # Set the odds ratio values above the points
    for i, odds_ratio in enumerate(plot_df['odds_ratio']):
        plt.text(odds_ratio, i, f'{odds_ratio:.3f}', va='bottom', ha='center', fontsize=10, color='black')

    # Set odds ratio 1 indicator
    plt.axvline(1, linestyle='--', linewidth=1)
    plt.xlabel('Odds Ratio')
    fig = plt.gcf()

    # Save fig as png
    plot_path = f'src/figures/{indicator}_odds_ratios.png'
    fig.savefig(plot_path, bbox_inches='tight')

    return plot_df, plot_path

def display_plot(df: pd.DataFrame, plot_path: str) -> None:
    """
    If the dataframe is not empty, display the odds ratio plot.
    """
    if df.empty:
        st.warning('No statistically significant associations found.')
    else:
        st.image(plot_path)
