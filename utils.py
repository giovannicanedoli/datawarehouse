import pandas as pd
country_map = {
    'PR': 'Puerto Rico', 'PS': 'Palestine', 'PT': 'Portugal', 'PY': 'Paraguay', 
    'AE': 'United Arab Emirates', 'AF': 'Afghanistan', 'AL': 'Albania', 'AM': 'Armenia', 
    'AO': 'Angola', 'AR': 'Argentina', 'AT': 'Austria', 'AU': 'Australia', 'AZ': 'Azerbaijan', 
    'RO': 'Romania', 'BA': 'Bosnia and Herzegovina', 'RS': 'Serbia', 'BD': 'Bangladesh', 
    'RU': 'Russia', 'BE': 'Belgium', 'BG': 'Bulgaria', 'BH': 'Bahrain', 'SA': 'Saudi Arabia', 
    'BR': 'Brazil', 'SC': 'Seychelles', 'SE': 'Sweden', 'SG': 'Singapore', 'SI': 'Slovenia', 
    'BY': 'Belarus', 'SK': 'Slovakia', 'BZ': 'Belize', 'CA': 'Canada', 'SV': 'El Salvador', 
    'CH': 'Switzerland', 'SZ': 'Eswatini', 'CL': 'Chile', 'CN': 'China', 'CO': 'Colombia', 
    'CR': 'Costa Rica', 'TH': 'Thailand', 'CY': 'Cyprus', 'CZ': 'Czech Republic', 
    'TR': 'Turkey', 'DE': 'Germany', 'TW': 'Taiwan', 'TZ': 'Tanzania', 'DK': 'Denmark', 
    'DO': 'Dominican Republic', 'UA': 'Ukraine', 'UG': 'Uganda', 'US': 'USA', 
    'EC': 'Ecuador', 'EE': 'Estonia', 'EG': 'Egypt', 'UZ': 'Uzbekistan', 'ES': 'Spain', 
    'VE': 'Venezuela', 'VG': 'British Virgin Islands', 'VN': 'Vietnam', 'FI': 'Finland', 
    'FR': 'France', 'GB': 'UK', 'GE': 'Georgia', 'GH': 'Ghana', 'GN': 'Guinea', 
    'GR': 'Greece', 'GT': 'Guatemala', 'HK': 'Hong Kong', 'HN': 'Honduras', 'HR': 'Croatia', 
    'YE': 'Yemen', 'HU': 'Hungary', 'ID': 'Indonesia', 'IE': 'Ireland', 'IL': 'Israel', 
    'IN': 'India', 'ZA': 'South Africa', 'IQ': 'Iraq', 'IR': 'Iran', 'IS': 'Iceland', 
    'IT': 'Italy', 'ZW': 'Zimbabwe', 'JO': 'Jordan', 'JP': 'Japan', 'KE': 'Kenya', 
    'KG': 'Kyrgyzstan', 'KH': 'Cambodia', 'KN': 'Saint Kitts and Nevis', 'KR': 'South Korea', 
    'KZ': 'Kazakhstan', 'LB': 'Lebanon', 'LK': 'Sri Lanka', 'LT': 'Lithuania', 
    'LU': 'Luxembourg', 'LV': 'Latvia', 'LY': 'Libya', 'MD': 'Moldova', 'MM': 'Myanmar', 
    'MN': 'Mongolia', 'MT': 'Malta', 'MV': 'Maldives', 'MX': 'Mexico', 'MY': 'Malaysia', 
    'MZ': 'Mozambique', 'NA': 'Namibia', 'NG': 'Nigeria', 'NI': 'Nicaragua', 'NL': 'Netherlands', 
    'NO': 'Norway', 'NP': 'Nepal', 'NZ': 'New Zealand', 'OM': 'Oman', 'PA': 'Panama', 
    'PE': 'Peru', 'PG': 'Papua New Guinea', 'PH': 'Philippines', 'PK': 'Pakistan', 'PL': 'Poland'
}

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

def categorize_industry(val):
    if pd.isna(val):
        return "Unknown"
    
    val_lower = str(val).lower().strip()
    
    # Priority Mapping
    
    # Finance
    if any(x in val_lower for x in ['bank', 'finance', 'financial']):
        return "Finance"
        
    # Healthcare
    if any(x in val_lower for x in ['health', 'medical', 'hospital']):
        return "Healthcare"

    # Technology
    if any(x in val_lower for x in ['tech', 'software', 'web', 'app', 'it', 'internet', 'data', 'computer', 'social networking', 'gaming', 'media']):
        return "Technology"
        
    # Retail
    if any(x in val_lower for x in ['retail', 'store', 'shop']):
        return "Retail"
        
    # Government
    if any(x in val_lower for x in ['government', 'state', 'public', 'military']):
        return "Government"
        
    # Education
    if any(x in val_lower for x in ['education', 'academic', 'school', 'university']):
        return "Education"
        
    # Telecom
    if any(x in val_lower for x in ['telecom']):
        return "Telecommunications"
        
    # Energy/Transport (Common enough to separate if needed, but for now group or Keep Other)
    if 'energy' in val_lower: return "Energy"
    if 'transport' in val_lower: return "Transport"
    
    return "Other"

def categorize_continent(val):
    if pd.isna(val):
        return "Unknown"
    
    val_lower = str(val).lower().strip()
    
    # Priority Mapping
    
    # North America
    if any(x in val_lower for x in ['north america', 'usa', 'canada']):
        return "North America"
        
    # South America
    if any(x in val_lower for x in ['south america']):
        return "South America"
        
    # Europe
    if any(x in val_lower for x in ['europe']):
        return "Europe"
        
    # Asia
    if any(x in val_lower for x in ['asia']):
        return "Asia"
        
    # Africa
    if any(x in val_lower for x in ['africa']):
        return "Africa"
        
    # Australia
    if any(x in val_lower for x in ['australia']):
        return "Australia"
        
    return "Other"

def categorize_nation_by_wealth(val):
    if pd.isna(val):
        return "Unknown"
    
    val_lower = str(val).lower().strip()
    
    # High Income
    if any(x in val_lower for x in ['usa', 'united states', 'uk', 'united kingdom', 'germany', 'france', 'japan', 'canada', 'australia', 'sweden', 'singapore', 'switzerland', 'norway', 'south korea', 'uae', 'saudi arabia', 'israel', 'qatar', 'netherlands', 'belgium', 'austria', 'finland', 'ireland', 'new zealand']):
        return "High Income"
        
    # Upper-Middle Income
    if any(x in val_lower for x in ['china', 'brazil', 'russia', 'mexico', 'turkey', 'argentina', 'south africa', 'thailand', 'malaysia', 'serbia', 'romania', 'bulgaria']):
        return "Upper-Middle Income"
        
    # Lower-Middle Income
    if any(x in val_lower for x in ['india', 'indonesia', 'vietnam', 'philippines', 'ukraine', 'pakistan', 'egypt', 'nigeria', 'uzbekistan', 'el salvador', 'morocco']):
        return "Lower-Middle Income"
        
    # Low Income
    if any(x in val_lower for x in ['ethiopia', 'uganda', 'tanzania', 'afghanistan', 'yemen', 'zimbabwe', 'mali', 'niger', 'syria', 'sudan']):
        return "Low Income"
        
    return "Other/Unknown"

def categorize_west_or_est_country(val):
    if pd.isna(val):
        return "Unknown"
    
    val_lower = str(val).lower().strip()
    
    # Western
    if any(x in val_lower for x in ['usa', 'united states', 'canada', 'uk', 'united kingdom', 'germany', 'france', 'italy', 'spain', 'australia', 'new zealand', 'europe', 'north america']):
        return "Western"
        
    # Eastern
    if any(x in val_lower for x in ['china', 'japan', 'korea', 'india', 'russia', 'asia', 'middle east', 'southeast asia', 'vietnam', 'thailand']):
        return "Eastern"
        
    return "Other/Unknown"