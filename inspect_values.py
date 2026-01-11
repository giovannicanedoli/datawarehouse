
import pandas as pd

try:
    df1 = pd.read_csv("organization_data_breaches.csv")
    print("=== df1 (organization_data_breaches) Method unique values ===")
    print(df1['Method'].unique())
except Exception as e:
    print(f"Error reading df1: {e}")

try:
    df2 = pd.read_csv("Global_Cybersecurity_Threats_2015-2024.csv")
    print("\n=== df2 (Global_Cybersecurity_Threats) Attack Type unique values ===")
    print(df2['Attack Type'].unique())
except Exception as e:
    print(f"Error reading df2: {e}")
