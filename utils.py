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
import pandas as pd

def categorize_continent(val):
    if pd.isna(val):
        return "Unknown"
    
    val_clean = str(val).strip()
    
    # Define Continent Sets
    continents = {
        "North America": {
            'USA', 'Canada', 'Mexico', 'Puerto Rico', 'Guatemala', 'Panama', 
            'Honduras', 'Costa Rica', 'El Salvador', 'Dominican Republic', 
            'Belize', 'British Virgin Islands', 'Saint Kitts and Nevis'
        },
        "South America": {
            'Brazil', 'Argentina', 'Colombia', 'Chile', 'Peru', 'Venezuela', 
            'Ecuador', 'Paraguay'
        },
        "Europe": {
            'UK', 'Italy', 'Germany', 'France', 'Spain', 'Netherlands', 'Russia', 
            'Ukraine', 'Poland', 'Sweden', 'Norway', 'Finland', 'Denmark', 
            'Ireland', 'Belgium', 'Switzerland', 'Austria', 'Greece', 'Portugal', 
            'Czech Republic', 'Slovakia', 'Hungary', 'Romania', 'Bulgaria', 
            'Serbia', 'Croatia', 'Slovenia', 'Lithuania', 'Latvia', 'Estonia', 
            'Belarus', 'Moldova', 'Albania', 'Bosnia and Herzegovina', 'Iceland', 
            'Luxembourg', 'Malta', 'Cyprus'
        },
        "Asia": {
            'China', 'Japan', 'India', 'South Korea', 'Taiwan', 'Hong Kong', 
            'Singapore', 'Malaysia', 'Thailand', 'Vietnam', 'Philippines', 
            'Indonesia', 'Pakistan', 'Bangladesh', 'Myanmar', 'Sri Lanka', 
            'Nepal', 'Maldives', 'Kazakhstan', 'Uzbekistan', 'Kyrgyzstan', 
            'Georgia', 'Armenia', 'Azerbaijan', 'Israel', 'Palestine', 'Jordan', 
            'Lebanon', 'Iraq', 'Saudi Arabia', 'United Arab Emirates', 'Oman', 
            'Bahrain', 'Yemen', 'Iran', 'Turkey', 'Cambodia'
        },
        "Africa": {
            'South Africa', 'Nigeria', 'Kenya', 'Egypt', 'Ghana', 'Tanzania', 
            'Uganda', 'Zimbabwe', 'Namibia', 'Angola', 'Mozambique', 'Eswatini', 
            'Seychelles', 'Libya', 'Guinea'
        },
        "Oceania": {
            'Australia', 'New Zealand', 'Papua New Guinea'
        }
    }

    # Direct match check
    for continent, country_list in continents.items():
        if val_clean in country_list:
            return continent
            
    return "Other"

def categorize_nation_by_welfare(val):
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
def split_year_range(val):
    """
    Splits 'YYYY-YYYY' into a list of years, or returns single year as list.
    """
    if pd.isna(val):
        return [val]
    if '-' not in str(val) and "and" not in str(val):
        return [val]
    if "and" in str(val):
        s_val = str(val).split('and')
        return [int(s_val[0].strip()), int(s_val[1].strip())]
    # - in the string
    s_val = str(val).split('-')
    # Create range inclusive
    return list(range(int(s_val[0]), int(s_val[1]) + 1))
def get_pandemic_era(year):
    """
    Distinguishes if a year is pre-pandemic or post-pandemic.
    Pandemic start is considered 2020.
    """
    if pd.isna(year):
        return "Unknown"
            
    year_int = int(year)
        
    if year_int < 2020:
        return "Pre-Pandemic"
    else:
        return "Post-Pandemic"
def is_leap_year(year):

    """
    Checks if a year is a leap year.
    Returns True/False or 'Unknown' on error.
    """
    if pd.isna(year):
        return "Unknown"
        
    year_int = int(year)
    
    # Leap year logic: divisible by 4, not by 100 unless also by 400
    if (year_int % 4 == 0 and year_int % 100 != 0) or (year_int % 400 == 0):
        return True
    else:
        return False

def remove_unknown_entries(val):
    """
    Replaces 'unknown' (case-insensitive) values with None.
    """
    if pd.isna(val):
        return None
        
    s_val = str(val).strip().lower()
    if s_val == "unknown" or s_val == "":
        return None
        
    return val