import pandas as pd
from utils import *

def load_breaches_data(filepath):
    """Processes Organization Data Breaches CSV."""
    df = pd.read_csv(filepath)
    df = df.drop(columns=["Sources"])
    
    # Standardize Time
    df['Year'] = df['Year'].apply(split_year_range)
    df = df.explode('Year')
    
    # Clean Records
    df['Records'] = df['Records'].apply(remove_unknown_entries)
    df['Records'] = (df['Records']
                     .astype(str)
                     .str.replace(',', '', regex=False)
                     .str.extract(r'(\d+)', expand=False))
    df['Records'] = pd.to_numeric(df['Records'], errors='coerce').fillna(0).astype(int)
    
    # Categorizations
    df['Unified_Attack_Category'] = df['Method'].apply(categorize_attack)
    df['Unified_Industry'] = df['Organization type'].apply(categorize_industry)
    df['Pandemic_Era'] = df['Year'].apply(get_pandemic_era)
    df['Is_Leap_Year'] = df['Year'].apply(is_leap_year)
    
    # Geographic Mapping
    df["Country"] = df["Entity"].map(entities_locations)
    df["Continent"] = df["Country"].apply(categorize_continent)
    df["Nation_Wealth"] = df["Country"].apply(categorize_nation_by_welfare)
    df["West_or_East"] = df["Country"].apply(categorize_west_or_est_country)
    
    return df.dropna()

def load_cyber_threats_data(filepath):
    """Processes Global Cybersecurity Threats CSV."""
    df = pd.read_csv(filepath)
    df = df.drop(columns=["Financial Loss (in Million $)"])
    
    # Categorizations
    df['Unified_Attack_Category'] = df['Attack Type'].apply(categorize_attack)
    df['Unified_Industry'] = df['Target Industry'].apply(categorize_industry)
    df["Continent"] = df["Country"].apply(categorize_continent)
    df["Nation_Wealth"] = df["Country"].apply(categorize_nation_by_welfare)
    df["West_or_East"] = df["Country"].apply(categorize_west_or_est_country)
    
    # Time Features
    df['Pandemic_Era'] = df['Year'].apply(get_pandemic_era)
    df['Is_Leap_Year'] = df['Year'].apply(is_leap_year)
    
    return df

def load_net_crime_data(filepath):
    """Processes Loss From Net Crime CSV (Reshaping & Cleaning)."""
    # keep_default_na=False prevents 'NA' (Namibia) from becoming NaN
    df = pd.read_csv(filepath, keep_default_na=False)
    df['Country'] = df['Country'].map(country_map)

    # Reshape: Melt and Pivot
    melted = df.melt(id_vars=['Country'], var_name='Metric', value_name='Value')
    melted[['Year', 'Type']] = melted['Metric'].str.extract(r'(\d{4})_(.*)')    
    
    unified = melted.pivot_table(
        index=['Country', 'Year'], 
        columns='Type', 
        values='Value', 
        aggfunc='first'
    ).reset_index()
    
    unified.columns.name = None 
    
    # Types and Features
    unified['Complaints'] = pd.to_numeric(unified['Complaints'], errors='coerce')
    unified['Losses'] = pd.to_numeric(unified['Losses'], errors='coerce')
    unified["Continent"] = unified["Country"].apply(categorize_continent)
    unified["Nation_Wealth"] = unified["Country"].apply(categorize_nation_by_welfare)
    unified["West_or_East"] = unified["Country"].apply(categorize_west_or_est_country)
    unified['Pandemic_Era'] = unified['Year'].apply(get_pandemic_era)
    unified['Is_Leap_Year'] = unified['Year'].apply(is_leap_year)
    
    return unified

def main():
    try:
        print("Processing Breaches...")
        df_breaches = load_breaches_data("data/organization_data_breaches.csv")
        
        print("Processing Global Threats...")
        df_threats = load_cyber_threats_data("data/Global_Cybersecurity_Threats_2015-2024.csv")
        
        print("Processing Net Crime...")
        df_net_crime = load_net_crime_data("data/LossFromNetCrime.csv")

        # Saving outputs
        print("Saving outputs...")
        df_breaches.to_csv("result/organization_data_breaches_unified.csv", index=False)
        df_threats.to_csv("result/Global_Cybersecurity_Threats_unified.csv", index=False)
        df_net_crime.to_csv("result/LossFromNetCrime_unified.csv", index=False)
        print("Cleanup complete.")

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()