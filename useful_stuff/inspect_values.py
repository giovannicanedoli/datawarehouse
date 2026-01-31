import pandas as pd

# Load the datasets
try:
    df1 = pd.read_csv("../data/Global_Cybersecurity_Threats_2015-2024.csv", keep_default_na=False)
    df2 = pd.read_csv("../data/LossFromNetCrime.csv", keep_default_na=False)
    df3 = pd.read_csv("../data/organization_data_breaches.csv")
    dfs = {"df1": df1, "df2": df2}
    
    entities = df3["Entity"].unique()
    print(entities)

except Exception as e:
    print(f"Error processing dataframes: {e}")
