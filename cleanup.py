
import pandas as pd
from unify_attacks import categorize_attack
from unify_industry import categorize_industry

def main():
    DEBUG = 0
    if DEBUG:
        print("=== df1 (organization_data_breaches) Method unique values ===")
        print(df1['Method'].unique())

        print("\n=== df2 (Global_Cybersecurity_Threats) Attack Type unique values ===")
        print(df2['Attack Type'].unique())
        

    try:
        df1 = pd.read_csv("organization_data_breaches.csv")
        df2 = pd.read_csv("Global_Cybersecurity_Threats_2015-2024.csv")
        df3 = pd.read_csv("LossFromNetCrime.csv")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    
    country_map = {
        'AE': 'United Arab Emirates', 'AF': 'Afghanistan', 'AL': 'Albania', 'AM': 'Armenia', 
        'AO': 'Angola', 'AR': 'Argentina', 'AT': 'Austria', 'AU': 'Australia', 'AZ': 'Azerbaijan',
        'BA': 'Bosnia and Herzegovina', 'BD': 'Bangladesh', 'BE': 'Belgium', 'BG': 'Bulgaria', 
        'BH': 'Bahrain', 'BY': 'Belarus', 'BZ': 'Belize', 'BR': 'Brazil', 'CA': 'Canada', 
        'CH': 'Switzerland', 'CL': 'Chile', 'CN': 'China', 'CO': 'Colombia', 'CR': 'Costa Rica', 
        'CY': 'Cyprus', 'CZ': 'Czech Republic', 'DE': 'Germany', 'DK': 'Denmark', 'DO': 'Dominican Republic',
        'EC': 'Ecuador', 'EE': 'Estonia', 'EG': 'Egypt', 'ES': 'Spain', 'FI': 'Finland', 
        'FR': 'France', 'GB': 'UK', 'GE': 'Georgia', 'GH': 'Ghana', 'GN': 'Guinea', 
        'GR': 'Greece', 'GT': 'Guatemala', 'HK': 'Hong Kong', 'HN': 'Honduras', 'HR': 'Croatia', 
        'HU': 'Hungary', 'ID': 'Indonesia', 'IE': 'Ireland', 'IL': 'Israel', 'IN': 'India', 
        'IQ': 'Iraq', 'IR': 'Iran', 'IS': 'Iceland', 'IT': 'Italy', 'JO': 'Jordan', 
        'JP': 'Japan', 'KE': 'Kenya', 'KG': 'Kyrgyzstan', 'KH': 'Cambodia', 'KN': 'Saint Kitts and Nevis', 
        'KR': 'South Korea', 'KZ': 'Kazakhstan', 'LB': 'Lebanon', 'LK': 'Sri Lanka', 'LT': 'Lithuania', 
        'LU': 'Luxembourg', 'LV': 'Latvia', 'LY': 'Libya', 'MD': 'Moldova', 'MM': 'Myanmar', 
        'MN': 'Mongolia', 'MT': 'Malta', 'MV': 'Maldives', 'MX': 'Mexico', 'MY': 'Malaysia', 
        'MZ': 'Mozambique', 'NG': 'Nigeria', 'NI': 'Nicaragua', 'NL': 'Netherlands', 'NO': 'Norway', 
        'NP': 'Nepal', 'NZ': 'New Zealand', 'OM': 'Oman', 'PA': 'Panama', 'PE': 'Peru', 
        'PG': 'Papua New Guinea', 'PH': 'Philippines', 'PK': 'Pakistan', 'PL': 'Poland', 
        'PR': 'Puerto Rico', 'PS': 'Palestine', 'PT': 'Portugal', 'PY': 'Paraguay', 'RO': 'Romania', 
        'RS': 'Serbia', 'RU': 'Russia', 'SA': 'Saudi Arabia', 'SC': 'Seychelles', 'SE': 'Sweden', 
        'SG': 'Singapore', 'SI': 'Slovenia', 'SK': 'Slovakia', 'SV': 'El Salvador', 'SZ': 'Eswatini', 
        'TH': 'Thailand', 'TR': 'Turkey', 'TW': 'Taiwan', 'TZ': 'Tanzania', 'UA': 'Ukraine', 
        'UG': 'Uganda', 'US': 'USA', 'UZ': 'Uzbekistan', 'VE': 'Venezuela', 'VG': 'British Virgin Islands', 
        'VN': 'Vietnam', 'YE': 'Yemen', 'ZA': 'South Africa', 'ZW': 'Zimbabwe'
    }

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

    print("\n=== Statistics per Year (df3) ===")
    stats = df3_unified.groupby('Year')[['Complaints', 'Losses']].agg(['mean', 'var', 'std'])
    print(stats)
    stats.to_csv("LossFromNetCrime_stats.csv")
    
    print("Processing df1 (Breaches)...")
    # df1 uses 'Method'
    df1['Unified_Attack_Category'] = df1['Method'].apply(categorize_attack)
    df1['Unified_Industry'] = df1['Organization type'].apply(categorize_industry)
    
    print("Processing df2 (Global Threats)...")
    # df2 uses 'Attack Type'
    df2['Unified_Attack_Category'] = df2['Attack Type'].apply(categorize_attack)
    df2['Unified_Industry'] = df2['Target Industry'].apply(categorize_industry)
    
    # Create the Dimension Map for reference
    # Get all unique values from both columns
    all_methods = pd.concat([df1['Method'].rename("Original_Value"), df2['Attack Type'].rename("Original_Value")]).unique()
    dim_df = pd.DataFrame({'Original_Value': all_methods})
    dim_df['Unified_Attack_Category'] = dim_df['Original_Value'].apply(categorize_attack)
    
    print("Saving outputs...")
    dim_df.to_csv("Dim_Attack_Map.csv", index=False)
    df1.to_csv("organization_data_breaches_unified.csv", index=False)
    df2.to_csv("Global_Cybersecurity_Threats_unified.csv", index=False)
    df3_unified.to_csv("LossFromNetCrime_unified.csv", index=False)
    
    print("Done.")
    print("\nSample Mapping:")
    print(dim_df.sample(10 if len(dim_df) > 10 else len(dim_df)))


if __name__ == "__main__":
    main()
