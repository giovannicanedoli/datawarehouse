import pandas as pd
import numpy as np

def categorize_attack(attack_val):
    if pd.isna(attack_val):
        return "Unknown"
    
    val_lower = str(attack_val).lower().strip()
    
    # Priority-based Mapping
    # 1. Active Hacking/Intrusion
    if any(x in val_lower for x in ['hacked', 'sql injection', 'ddos', 'man-in-the-middle', 'zero-day', 'vulnerabilities', 'rogue contractor']):
        return "Hacking/Intrusion"
    
    # 2. Malware/Ransomware
    if any(x in val_lower for x in ['malware', 'ransomware']):
        return "Malware"
    
    # 3. Social Engineering
    if any(x in val_lower for x in ['phishing', 'social engineering']):
        return "Social Engineering"
    
    # 4. Misconfiguration / Poor Security (if not already caught by hacked)
    # Note: "poor security / hacked" is caught by Hacking above.
    if any(x in val_lower for x in ['poor security', 'misconfiguration', 'unsecured', 'unprotected', 'improper setting', 'publicly accessible']):
        return "Misconfiguration/Vulnerability"
        
    # 5. Insider Threat
    if any(x in val_lower for x in ['inside job']):
        return "Insider Threat"
        
    # 6. Physical Loss
    if any(x in val_lower for x in ['lost', 'stolen']):
        return "Physical Loss"
        
    # 7. Accidental
    if any(x in val_lower for x in ['accidentally', 'published', 'exposed']):
        return "Accidental/Error"
        
    return "Other/Unknown"

def main():
    print("Loading datasets...")
    try:
        df1 = pd.read_csv("data/organization_data_breaches.csv")
        df2 = pd.read_csv("data/Global_Cybersecurity_Threats_2015-2024.csv")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    print("Processing df1 (Breaches)...")
    # df1 uses 'Method'
    df1['Unified_Attack_Category'] = df1['Method'].apply(categorize_attack)
    
    print("Processing df2 (Global Threats)...")
    # df2 uses 'Attack Type'
    df2['Unified_Attack_Category'] = df2['Attack Type'].apply(categorize_attack)
    
    # Create the Dimension Map for reference
    # Get all unique values from both columns
    all_methods = pd.concat([df1['Method'].rename("Original_Value"), df2['Attack Type'].rename("Original_Value")]).unique()
    dim_df = pd.DataFrame({'Original_Value': all_methods})
    print(dim_df)
    dim_df['Unified_Attack_Category'] = dim_df['Original_Value'].apply(categorize_attack)
    print(dim_df)
    
    df1 = df1.drop(columns=["Entity", "Year" ,"Records","Organization type","Sources"])
    df2 = df2.drop(columns=["Country","Year","Target Industry","Financial Loss (in Million $)","Number of Affected Users","Attack Source","Security Vulnerability Type","Defense Mechanism Used","Incident Resolution Time (in Hours)"])
    print("Saving outputs...")
    dim_df.to_csv("test/Dim_Attack_Map.csv", index=False)
    df1.to_csv("test/organization_data_breaches_unified.csv", index=False)
    df2.to_csv("test/Global_Cybersecurity_Threats_unified.csv", index=False)
    
if __name__ == "__main__":
    main()
