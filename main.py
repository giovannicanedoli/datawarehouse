import pandas as pd
from utils import country_map, categorize_attack, categorize_industry

def main():
    DEBUG = 0
    if DEBUG:
        print("=== df1 (organization_data_breaches) Method unique values ===")
        print(df1['Method'].unique())

        print("\n=== df2 (Global_Cybersecurity_Threats) Attack Type unique values ===")
        print(df2['Attack Type'].unique())
        

    try:
        df1 = pd.read_csv("data/organization_data_breaches.csv")
        df2 = pd.read_csv("data/Global_Cybersecurity_Threats_2015-2024.csv")
        df3 = pd.read_csv("data/LossFromNetCrime.csv")
    except FileNotFoundError as e:
        print(f"Error while opening one or more files: {e}")
        return

    print("Processing df3 (Net Crime)...")
    df3['Country'] = df3['Country'].map(country_map)
    
    # Reshape df3: Melt and Pivot to get Country, Year, Complaints, Losses
    print("Standardizing Time for df3...")
    df3_melted = df3.melt(id_vars=['Country'], var_name='Metric', value_name='Value')
    # Metric is like "2019_Complaints" or "2019_Losses"
    # Extract Year d{4} and Type after _
    df3_melted[['Year', 'Type']] = df3_melted['Metric'].str.extract(r'(\d{4})_(.*)')    
    
    # Pivot to make Complaints and Losses columns
    df3_unified = df3_melted.pivot_table(index=['Country', 'Year'], columns='Type', values='Value', aggfunc='first').reset_index()
    # Columns will be Country, Year, Complaints, Losses
    df3_unified.columns.name = None # Clean up index name
    
    # Ensure numeric types
    df3_unified['Complaints'] = pd.to_numeric(df3_unified['Complaints'], errors='coerce')
    df3_unified['Losses'] = pd.to_numeric(df3_unified['Losses'], errors='coerce')

    # Cleaning unused data
    print("Cleaning unused data...")
    df1 = df1.drop(columns=["Sources"])
    df2 = df2.drop(columns=["Financial Loss (in Million $)"])
    
    
    print("Processing df1 (Breaches)...")
    # df1 uses 'Method'
    df1['Unified_Attack_Category'] = df1['Method'].apply(categorize_attack)
    df1['Unified_Industry'] = df1['Organization type'].apply(categorize_industry)
    
    print("Processing df2 (Global Threats)...")
    # df2 uses 'Attack Type'
    df2['Unified_Attack_Category'] = df2['Attack Type'].apply(categorize_attack)
    df2['Unified_Industry'] = df2['Target Industry'].apply(categorize_industry)

    print("Saving outputs...")
    
    df1.to_csv("result/organization_data_breaches_unified.csv", index=False)
    df2.to_csv("result/Global_Cybersecurity_Threats_unified.csv", index=False)
    df3_unified.to_csv("result/LossFromNetCrime_unified.csv", index=False)

    if DEBUG:
        print("Done.")
        print("\nSample Mapping:")
        print(dim_df.sample(10 if len(dim_df) > 10 else len(dim_df)))


if __name__ == "__main__":
    main()
