import pandas as pd
from utils import *
def main():
    DEBUG = 0
    if DEBUG:
        print("=== df1 (organization_data_breaches) Method unique values ===")
        print(df1['Method'].unique())

        print("\n=== df2 (Global_Cybersecurity_Threats) Attack Type unique values ===")
        print(df2['Attack Type'].unique())

        countries = set(df2['Country'].unique())
        countries_2 = set(df3['Country'].unique())
        print(f"Unique countries in the dataset: {countries.union(countries_2)}")
            

    try:
        df1 = pd.read_csv("data/organization_data_breaches.csv")
        df2 = pd.read_csv("data/Global_Cybersecurity_Threats_2015-2024.csv")
        df3 = pd.read_csv("data/LossFromNetCrime.csv", keep_default_na=False) #Namibia NA is interpreted as NaN
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

    # Add geography
    df3_unified["Continent"] = df3_unified["Country"].apply(categorize_continent)
    df3_unified["Nation_Wealth"] = df3_unified["Country"].apply(categorize_nation_by_welfare)
    df3_unified["West_or_East"] = df3_unified["Country"].apply(categorize_west_or_est_country)
    
    # Add Time Features to df3
    df3_unified['Pandemic_Era'] = df3_unified['Year'].apply(get_pandemic_era)
    df3_unified['Is_Leap_Year'] = df3_unified['Year'].apply(is_leap_year)

    # Cleaning unused data
    print("Cleaning unused data...")
    df1 = df1.drop(columns=["Sources"])
    df2 = df2.drop(columns=["Financial Loss (in Million $)"])
    
    
    print("Processing df1 (Breaches)...")
    
    # Convert Year to list of years and explode
    df1['Year'] = df1['Year'].apply(split_year_range)
    #trasforming the list of years into multiple rows egs [2019, 2020] -> [2019], [2020]
    df1 = df1.explode('Year')
    
    # Clean Records (remove 'unknown') and extract numbers
    df1['Records'] = df1['Records'].apply(remove_unknown_entries)
    # Extract numbers (remove commas, take first sequence of digits)
    # This turns "9,000,000 (approx)" into "9000000"
    df1['Records'] = df1['Records'].astype(str).str.replace(',', '', regex=False).str.extract(r'(\d+)', expand=False)
    # Fill NaNs with 0 to allow SUM
    df1['Records'] = pd.to_numeric(df1['Records'], errors='coerce').fillna(0).astype(int)
    
    # df1 uses 'Method'
    df1['Unified_Attack_Category'] = df1['Method'].apply(categorize_attack)
    df1['Unified_Industry'] = df1['Organization type'].apply(categorize_industry)
    # Add Time Features to df1
    df1['Pandemic_Era'] = df1['Year'].apply(get_pandemic_era)
    df1['Is_Leap_Year'] = df1['Year'].apply(is_leap_year)
    
    # Add country Feature to df1

    df1["Country"] = df1["Entity"].map(entities_locations)
    df1["Continent"] = df1["Country"].apply(categorize_continent)
    df1["Nation_Wealth"] = df1["Country"].apply(categorize_nation_by_welfare)
    df1["West_or_East"] = df1["Country"].apply(categorize_west_or_est_country)

    print("map confirmed")

    
    print("Processing df2 (Global Threats)...")
    # df2 uses 'Attack Type'
    df2['Unified_Attack_Category'] = df2['Attack Type'].apply(categorize_attack)
    df2['Unified_Industry'] = df2['Target Industry'].apply(categorize_industry)

    df2["Continent"] = df2["Country"].apply(categorize_continent)
    df2["Nation_Wealth"] = df2["Country"].apply(categorize_nation_by_welfare)
    df2["West_or_East"] = df2["Country"].apply(categorize_west_or_est_country)


    # Add Time Features to df2
    df2['Pandemic_Era'] = df2['Year'].apply(get_pandemic_era)
    df2['Is_Leap_Year'] = df2['Year'].apply(is_leap_year)

    #remove null values from df1
    df1 = df1.dropna()

    # df1['Records'] = df1['Records'].replace('unknown', '')

    print("Saving outputs...")
    
    df1.to_csv("result/organization_data_breaches_unified.csv", index=False)
    df2.to_csv("result/Global_Cybersecurity_Threats_unified.csv", index=False)
    df3_unified.to_csv("result/LossFromNetCrime_unified.csv", index=False)



if __name__ == "__main__":
    main()
