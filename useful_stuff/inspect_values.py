import pandas as pd

# Load the datasets
try:
    df1 = pd.read_csv("../data/LossFromNetCrime.csv", keep_default_na=False)
    
    dfs = {"df1": df1, "df2": df2, "df3": df3}

    for name, df in dfs.items():
        print(f"--- Analyzing {name} ---")
        has_nan = False
        for column in df.columns:
            if df[column].isnull().any():
                print(f"FOUND: Column '{column}' contains NaN values.")
                has_nan = True
        
        if not has_nan:
            print("No NaN values found in this DataFrame.")
        print()

except Exception as e:
    print(f"Error processing dataframes: {e}")
