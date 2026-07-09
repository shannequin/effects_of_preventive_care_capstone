import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from utils.custom_visuals import rainbow_divider


CONN = st.connection("postgresql", type="sql")

def populate_body():
    query = """SELECT
                    hadsigm4,
                    colncncr,
                    vircolo1,
                    smalstol,
                    stooldn2,
                    primins2
                FROM staging.behavioral_risk_factor_surveillance_system
                WHERE primins2 IS NOT NULL
	            AND hadsigm4 IS NOT NULL
                OR colncncr IS NOT NULL
                OR vircolo1 IS NOT NULL
                OR smalstol IS NOT NULL
                OR stooldn2 IS NOT NULL;"""

    colon_df = CONN.query(sql=query)

    colon_df['ANY_PREVENTIVE_CARE'] = colon_df[['hadsigm4', 'colncncr', 'vircolo1', 'smalstol']].apply(
        lambda row: 1 if 'Yes' in row.values else 0, axis=1
    )
    model = smf.logit(formula="ANY_PREVENTIVE_CARE ~ C(primins2)", data=colon_df).fit()

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import textwrap

    # Get coefficient table from fitted statsmodels object
    params = model.params
    conf = model.conf_int()
    pvalues = model.pvalues

    # Build plotting dataframe
    plot_df = pd.DataFrame({
        "term": params.index,
        "coef": params.values,
        "ci_lower": conf[0].values,
        "ci_upper": conf[1].values,
        "p_value": pvalues.values
    })

    # Remove intercept
    plot_df = plot_df[plot_df["term"] != "Intercept"].copy()

    # Convert log-odds to odds ratios
    plot_df["odds_ratio"] = np.exp(plot_df["coef"])
    plot_df["or_ci_lower"] = np.exp(plot_df["ci_lower"])
    plot_df["or_ci_upper"] = np.exp(plot_df["ci_upper"])

    # Clean long statsmodels categorical labels
    plot_df["label"] = (
        plot_df["term"]
        .str.replace(r"C\(primins2\)\[T\.", "", regex=True)
        .str.replace(r"\]$", "", regex=True)
    )

    # Optional: wrap long labels
    plot_df["label"] = plot_df["label"].apply(lambda x: "\n".join(textwrap.wrap(x, width=45)))

    # Sort by odds ratio
    plot_df = plot_df.sort_values("odds_ratio")

    # Plot
    plt.figure(figsize=(10, 8))

    plt.errorbar(
        x=plot_df["odds_ratio"],
        y=plot_df["label"],
        xerr=[
            plot_df["odds_ratio"] - plot_df["or_ci_lower"],
            plot_df["or_ci_upper"] - plot_df["odds_ratio"]
        ],
        fmt="o",
        capsize=4
    )

    # Reference line: odds ratio = 1
    plt.axvline(1, linestyle="--", linewidth=1)

    plt.xscale("log")
    plt.xlabel("Odds Ratio, log scale")
    plt.ylabel("Insurance Type")
    plt.title("Odds Ratios for Preventive Care by Primary Insurance Type")
    fig = plt.gcf()
    st.pyplot(fig, width="stretch")

    st.text(model.summary())

def main() -> None:
    """
    Display the Analysis page.
    """

    st.title("Analysis", text_alignment="center")

    rainbow_divider()

    populate_body()


if __name__ == "__main__":
    main()