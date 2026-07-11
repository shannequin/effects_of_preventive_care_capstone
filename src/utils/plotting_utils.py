import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import streamlit as st
import textwrap


def plot_nhis_survey(selected_survey: str, selected_demographic: str, survey_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a line plot of the NHIS survey trends.
    """
    # Filter the survey dataframe based on the selected demographic
    survey_df = survey_df.loc[survey_df['demographic_group'] == selected_demographic]
    survey_df = survey_df.dropna(subset=['period']).copy()

    # Drop unnecessary columns and sort the dataframe for better display
    survey_df = (
        survey_df
        .drop(columns=['code', 'title', 'demographic_group'])
        .sort_values(['population', 'period'])
    )

    # Convert period to a string for better display on the x-axis
    try:
        survey_df['period'] = survey_df['period'].astype(int).astype(str)
    except:
        survey_df['period'] = survey_df['period'].astype(str)

    values = ''

    # If estimate column exists, convert it to numeric for plotting
    if 'estimate' in survey_df.columns:
        # Convert the estimate column to numeric, coercing errors to NaN
        survey_df['estimate'] = pd.to_numeric(survey_df['estimate'], errors='coerce')
        values = 'estimate'
        y_label = 'Estimate (%)'

    # Create a matrix of period vs population with the estimate as the values
    survey_df = survey_df.pivot(
        index='period',
        columns='population',
        values=values
    )

    if survey_df.empty:
        st.warning('No data available for the selected survey and demographic group.')
        return pd.DataFrame()
    
    else:
        # Initialize the figure and axis    
        fig, ax = plt.subplots()

        title = ''
        if 'cancer' in selected_survey.lower():
            title = 'Screening Rate (%)'

        # Create a line plot of the survey data
        survey_df.plot(ax=ax, marker='o')

        # Set labels
        ax.set_title(f'{selected_survey} {title} by {selected_demographic}')
        ax.set_xlabel('Period')
        ax.set_ylabel(y_label)
        ax.legend(title='Population', bbox_to_anchor=(1, 1), loc='upper left')
        ax.set_xticks(range(len(survey_df.index)))
        ax.set_xticklabels(survey_df.index, rotation=45)

        # Display the plot in Streamlit
        st.pyplot(fig)

        # Save the plot as a PNG file
        # Format the demographic name for the file path and lowercase
        # Replace blank space with underscore and remove special characters for better file naming
        survey_name = re.sub(r'[\*\^\\\[\]/]', '', selected_survey).lower()
        survey_name = survey_name.replace(' ', '_').lower()
        demographic_name = re.sub(r'[\*\^\\\[\]/]', '', selected_demographic).lower()
        demographic_name = demographic_name.replace(' ', '_').lower()
        plot_path = f'src/figures/{survey_name}_{demographic_name}_survey.png'
        fig.savefig(plot_path, bbox_inches='tight')

        return survey_df

def plot_odds_ratio(model, indicator: str) -> tuple[pd.DataFrame, str]:
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

    # Wrap long labels for better display
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

    # Label the x-axis
    plt.xlabel('Odds Ratio')

    # Get the current figure
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
