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
