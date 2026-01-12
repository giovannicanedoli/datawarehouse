import pandas as pd
from utils import country_map

try:
    df1 = pd.read_csv("data/LossFromNetCrime.csv")
    print("=== df1 (LossFromNetCrime) Method unique values ===")
    df1["Country"] = df1["Country"].map(country_map)
    print(df1['Country'].unique())


    df2 = pd.read_csv("data/Global_Cybersecurity_Threats_2015-2024.csv")
    print("=== df2 (Global_Cybersecurity_Threats) Method unique values ===")
    print(df2['Country'].unique())

    print(set(df1["Country"]).symmetric_difference(set(df2["Country"])))

    # val1 = df1['Method'].unique()
    # try:
    #     df2 = pd.read_csv("data/Global_Cybersecurity_Threats_2015-2024.csv")
    #     print("\n=== df2 (Global_Cybersecurity_Threats) Attack Type unique values ===")
    #     print(df2['Attack Type'].unique())
    #     val2 = df2["Attack Type"].unique()
    #     print(set(val1).symmetric_difference(set(val2)))

    # except Exception as e:
    #     print(f"Error reading df2: {e}")
except Exception as e:
    print(f"Error reading df1: {e}")



