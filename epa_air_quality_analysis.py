"""
EPA Air Quality Analysis

Portfolio project adapted from completed EPA air-quality coursework.
The analysis uses Python, pandas, and NumPy to explore Air Quality Index
(AQI) observations by state and county, compare geographic patterns, and
identify readings that warrant closer examination.

Data source:
https://raw.githubusercontent.com/adacert/EPA/main/c2_epa_air_quality.csv
"""

import numpy as np
import pandas as pd


DATA_URL = "https://raw.githubusercontent.com/adacert/EPA/main/c2_epa_air_quality.csv"


def load_data(url=DATA_URL):
    """Load EPA AQI data into a pandas DataFrame."""
    return pd.read_csv(url)


def county_counter(data, state):
    """Return the number of AQI observations for each county in a state."""
    state_data = data[data["state_name"] == state]
    return state_data["county_name"].value_counts().to_dict()


def main():
    # Load and inspect the dataset.
    epa_df = load_data()

    print("EPA AIR QUALITY ANALYSIS")
    print("=" * 50)
    print(f"Total observations: {len(epa_df):,}")
    print("\nFirst five rows:")
    print(epa_df.head())

    print("\nDataset information:")
    epa_df.info()

    print("\nAQI summary statistics:")
    print(epa_df["aqi"].describe())

    # Focus on California, Texas, and Pennsylvania, the three states used
    # in the original pandas analysis.
    focus_states = ["California", "Texas", "Pennsylvania"]
    top3 = epa_df[epa_df["state_name"].isin(focus_states)].copy()

    print("\nObservations by focus state:")
    print(top3["state_name"].value_counts())

    # Sort observations from highest to lowest AQI.
    top3_sorted = top3.sort_values(by="aqi", ascending=False)
    print("\nTen highest AQI observations in the focus states:")
    print(top3_sorted.head(10))

    # Examine California observations.
    ca_df = top3_sorted[top3_sorted["state_name"] == "California"].copy()
    print(f"\nCalifornia observations: {len(ca_df):,}")

    print("\nMost frequently represented California counties:")
    print(ca_df["county_name"].value_counts().head(10))

    la_mean_aqi = ca_df.loc[
        ca_df["county_name"] == "Los Angeles", "aqi"
    ].mean()
    print(f"\nLos Angeles County mean AQI: {la_mean_aqi:.2f}")

    # Compare mean AQI across the three focus states.
    state_mean_aqi = (
        top3.groupby("state_name")["aqi"]
        .mean()
        .sort_values(ascending=False)
    )
    print("\nMean AQI by focus state:")
    print(state_mean_aqi.round(2))

    # Use a reusable function to count county observations for a state.
    florida_counties = county_counter(epa_df, "Florida")
    print("\nFlorida county observation counts:")
    print(florida_counties)

    # Identify Washington observations with AQI of 51 or greater.
    washington_51_plus = epa_df[
        (epa_df["state_name"] == "Washington") & (epa_df["aqi"] >= 51)
    ]
    print("\nWashington observations with AQI >= 51:")
    print(washington_51_plus)

    # NumPy analysis of AQI values.
    aqi_array = epa_df["aqi"].dropna().to_numpy()

    print("\nNumPy AQI summary:")
    print(f"Maximum AQI: {np.max(aqi_array):.2f}")
    print(f"Minimum AQI: {np.min(aqi_array):.2f}")
    print(f"Median AQI: {np.median(aqi_array):.2f}")
    print(f"Standard deviation: {np.std(aqi_array):.2f}")

    # Calculate the share of readings at AQI 5 or below.
    percent_under_6 = (aqi_array <= 5).sum() / len(aqi_array)
    print(f"Readings with AQI <= 5: {percent_under_6:.2%}")

    print("\nKEY TAKEAWAYS")
    print("- Compared AQI patterns across California, Texas, and Pennsylvania.")
    print("- Examined California county-level observations and Los Angeles mean AQI.")
    print("- Isolated Washington readings with AQI values of 51 or greater.")
    print("- Used NumPy to calculate AQI distribution statistics and threshold shares.")


if __name__ == "__main__":
    main()
