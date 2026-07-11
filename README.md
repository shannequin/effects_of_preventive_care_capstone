# Data Science Capstone

## Project Summary: Preventive Care

This project analyzes preventive care access using survey data, with a focus on how demographic and socioeconomic factors relate to preventive screening behavior. The project includes data ingestion, cleaning, exploratory analysis, statistical modeling, and visualization through a Streamlit application.

## Key Questions

- Are insurance types significantly associated with receiving care?
- Which groups appear to have lower odds of receiving preventive screening?

## Data

The project uses Behavioral Risk Factor Surveillance System survey data. Relevant fields include preventive screening responses, insurance type, income level, education level, sex, and other demographic variables.

Data files intended for ingestion should be stored outside version control in:

```text
data_to_ingest/
````

## Methods

- Data ETL from raw files to PostgreSQL
- Data ingestion from PostgreSQL
- Data cleaning and categorical mapping
- Exploratory data analysis
- Logistic regression using `statsmodels`
- Odds ratio interpretation
- Predicted probability visualization
- Interactive Streamlit dashboard development

## Tech Stack

- Python
- Pandas
- NumPy
- SQLAlchemy
- PostgreSQL
- Statsmodels
- Matplotlib
- Streamlit
- Conda

## Running the Project Locally

Run the Streamlit app from the project root:

```bash
streamlit run src/Overview.py
```

## Environment Setup

Create a Conda environment export:

```bash
conda env export > environment.yml
```

Create a pip requirements file:

```bash
pip list --format=freeze > requirements.txt
```

Create a `.env` file for local environment variables.

Set the Python interpreter to the Conda environment.

Set the project root on the Python search path:

```bash
set PYTHONPATH=<set root>\effects_of_preventive_care_capstone
```

## Notes

Process documentation is maintained in Google Docs:

[https://docs.google.com/document/d/1v-E5yx_0U507c50uh5mUwsKBTDiMeami7YytXxGiHFA/edit?usp=sharing](https://docs.google.com/document/d/1v-E5yx_0U507c50uh5mUwsKBTDiMeami7YytXxGiHFA/edit?usp=sharing)

Add the following files and folders to `.gitignore`:

```text
src/.streamlit/secrets.toml
data_to_ingest/
```

## Engineering Note

I am especially proud of the engineering that went into this project. Beyond the analysis itself, I focused on building a structured, maintainable application with reusable functions, organized data workflows, database integration, environment configuration, and a Streamlit interface that makes the results easier to explore. This project challenged me to think not only like a data scientist, but also like a data engineer, software engineer, and architect responsible for creating a reliable and understandable end-to-end product.