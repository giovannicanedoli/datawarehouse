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

entities_locations = {
    "50 companies and government institutions": "USA",
    "2018 British Airways cyberattack": "UK",
    "2019 Bulgarian revenue agency hack": "Bulgaria",
    "Adobe Inc.": "USA",
    "Adobe Systems Incorporated": "USA",
    "Advocate Medical Group": "USA",
    "AerServ (subsidiary of InMobi)": "USA",
    "Affinity Health Plan, Inc.": "USA",
    "Air Canada": "Canada",
    "Airtel": "India",
    "Amazon Japan G.K.": "Japan",
    "Ancestry.com": "USA",
    "Animal Jam": "USA",
    "Ankle & Foot Center of Tampa Bay, Inc.": "USA",
    "Anthem Inc.": "USA",
    "AOL": "USA",
    "Apple": "USA",
    "Apple Health Medicaid": "USA",
    "Apple, Inc./BlueToad": "USA",
    "Ashley Madison": "Canada",
    "AT&T": "USA",
    "Atraf": "Israel",
    "Auction.co.kr": "South Korea",
    "Australian Immigration Department": "Australia",
    "Australian National University": "Australia",
    "Automatic Data Processing": "USA",
    "AvMed, Inc.": "USA",
    "Bailey's Inc.": "USA",
    "Bank of America": "USA",
    "Barnes & Noble": "USA",
    "Bell Canada": "Canada",
    "Benesse": "Japan",
    "Betfair": "UK",
    "Bethesda Game Studios": "USA",
    "Betsson Group": "Malta",
    "Blank Media Games": "USA",
    "Blizzard Entertainment": "USA",
    "BlueCross BlueShield of Tennessee": "USA",
    "BMO and Simplii": "Canada",
    "British Airways": "UK",
    "California Department of Child Support Services": "USA",
    "Canva": "Australia",
    "Capcom": "Japan",
    "Capital One": "USA",
    "CardSystems Solutions Inc. (MasterCard, Visa, Discover Financial Services and American Express)": "USA",
    "Cathay Pacific Airways": "Hong Kong",
    "CareFirst BlueCross Blue Shield - Maryland": "USA",
    "Central Coast Credit Union": "Australia",
    "Central Hudson Gas & Electric": "USA",
    "CheckFree Corporation": "USA",
    "CheckPeople": "USA",
    "China Software Developer Network": "China",
    "Chinese gaming websites (three: Duowan, 7K7K, 178.com)": "China",
    "Citigroup": "USA",
    "City and Hackney Teaching Primary Care Trust": "UK",
    "Clearview AI": "USA",
    "Colorado government": "USA",
    "Community Health Systems": "USA",
    "Philippines Commission on Elections": "Philippines",
    "Compass Bank": "USA",
    "Countrywide Financial Corp": "USA",
    "Centers for Medicare & Medicaid Services": "USA",
    "Cox Communications": "USA",
    "Crescent Health Inc., Walgreens": "USA",
    "CVS": "USA",
    "CyberServe": "Israel",
    "Dai Nippon Printing": "Japan",
    "Data Processors International (MasterCard, Visa, Discover Financial Services and American Express)": "USA",
    "Defense Integrated Data Center (South Korea)": "South Korea",
    "Dedalus": "Italy",
    "Deloitte": "UK",
    "Democratic National Committee": "USA",
    "US Department of Homeland Security": "USA",
    "Desjardins": "Canada",
    "Domino's Pizza (France)": "France",
    "DoorDash": "USA",
    "UK Driving Standards Agency": "UK",
    "Dropbox": "USA",
    "Drupal": "USA",
    "DSW Inc.": "USA",
    "Dubsmash": "USA",
    "Dun & Bradstreet": "USA",
    "EasyJet": "UK",
    "eBay": "USA",
    "Earl Enterprises(Buca di Beppo, Earl of Sandwich, Planet Hollywood,Chicken Guy, Mixology, Tequila Taqueria)": "USA",
    "Educational Credit Management Corporation": "USA",
    "Eisenhower Medical Center": "USA",
    "ElasticSearch": "USA",
    "Embassy Cables": "USA",
    "Emergency Healthcare Physicians, Ltd.": "USA",
    "Emory Healthcare": "USA",
    "Equifax": "USA",
    "European Central Bank": "Germany",
    "Evernote": "USA",
    "Exactis": "USA",
    "Excellus BlueCross BlueShield": "USA",
    "Experian - T-Mobile US": "USA",
    "EyeWire": "USA",
    "Facebook": "USA",
    "Fast Retailing": "Japan",
    "Federal Reserve Bank of Cleveland": "USA",
    "Fidelity National Information Services": "USA",
    "First American Corporation": "USA",
    "FireEye": "USA",
    "Florida Department of Juvenile Justice": "USA",
    "Friend Finder Networks": "USA",
    "Funimation": "USA",
    "Formspring": "USA",
    "Unknown": "Unknown",
    "Gamigo": "Germany",
    "Gap Inc.": "USA",
    "Gawker": "USA",
    "Global Payments": "USA",
    "Gmail": "USA",
    "Google Plus": "USA",
    "Greek government": "Greece",
    "Grozio Chirurgija": "Lithuania",
    "GS Caltex": "South Korea",
    "Gyft": "USA",
    "Hannaford Brothers Supermarket Chain": "USA",
    "HauteLook": "USA",
    "Health Net": "USA",
    "Health Net\xa0— IBM": "USA",
    "Health Sciences Authority (Singapore)": "Singapore",
    "Health Service Executive": "Ireland",
    "Heartland": "USA",
    "Heathrow Airport": "UK",
    "Hewlett Packard": "USA",
    "Hilton Hotels": "USA",
    "Home Depot": "USA",
    "Honda Canada": "Canada",
    "Hyatt Hotels": "USA",
    "Iberdrola": "Spain",
    "Instagram": "USA",
    "Internal Revenue Service": "USA",
    "International Committee of the Red Cross": "Switzerland",
    "Inuvik hospital": "Canada",
    "Iranian banks (three: Saderat, Eghtesad Novin, and Saman)": "Iran",
    "Japan Pension Service": "Japan",
    "Japanet Takata": "Japan",
    "Jefferson County, West Virginia": "USA",
    "JP Morgan Chase": "USA",
    "Justdial": "India",
    "KDDI": "Japan",
    "Kirkwood Community College": "USA",
    "KM.RU": "Russia",
    "Koodo Mobile": "Canada",
    "Korea Credit Bureau": "South Korea",
    "Kroll Background America": "USA",
    "KT Corporation": "South Korea",
    "LexisNexis": "USA",
    "Landry's, Inc.": "USA",
    "Les Éditions Protégez-vous": "Canada",
    "LifeLabs": "Canada",
    "Lincoln Medical & Mental Health Center": "USA",
    "LinkedIn, eHarmony, Last.fm": "USA",
    "Living Social": "USA",
    "MacRumors.com": "USA",
    "Mandarin Oriental Hotels": "Hong Kong",
    "Marriott International": "USA",
    "Massachusetts Government": "USA",
    "Massive American business hack including 7-Eleven and Nasdaq": "USA",
    "US Medicaid": "USA",
    "Medical Informatics Engineering": "USA",
    "Memorial Healthcare System": "USA",
    "Michaels": "USA",
    "Microsoft": "USA",
    "Microsoft Exchange servers": "USA",
    "Militarysingles.com": "USA",
    "Ministry of Education (Chile)": "Chile",
    "Ministry of Health (Singapore)": "Singapore",
    "Mitsubishi Tokyo UFJ Bank": "Japan",
    "MongoDB": "USA",
    "Mobile TeleSystems (MTS)": "Russia",
    "Monster.com": "USA",
    "Morgan Stanley Smith Barney": "USA",
    "Morinaga Confectionery": "Japan",
    "Mozilla": "USA",
    "MyHeritage": "Israel",
    "NASDAQ": "USA",
    "Natural Grocers": "USA",
    "NEC Networks, LLC": "USA",
    "Neiman Marcus": "USA",
    "Nemours Foundation": "USA",
    "Network Solutions": "USA",
    "New York City Health & Hospitals Corp.": "USA",
    "New York State Electric & Gas": "USA",
    "New York Taxis": "USA",
    "Nexon Korea Corp": "South Korea",
    "NHS": "UK",
    "Nintendo (Club Nintendo)": "Japan",
    "Nintendo (Nintendo Account)": "Japan",
    "Nippon Television": "Japan",
    "Nival Networks": "Cyprus",
    "Norwegian Tax Administration": "Norway",
    "Now:Pensions": "UK",
    "Ofcom": "UK",
    "US Office of Personnel Management": "USA",
    "Office of the Texas Attorney General": "USA",
    "Ohio State University": "USA",
    "Orbitz": "USA",
    "Oregon Department of Transportation": "USA",
    "OVH": "France",
    "Patreon": "USA",
    "PayPay": "Japan",
    "Popsugar": "USA",
    "Premera": "USA",
    "Puerto Rico Department of Health": "USA",
    "Quest Diagnostics": "USA",
    "Quora": "USA",
    "Rakuten": "Japan",
    "Rambler.ru": "Russia",
    "RBS Worldpay": "UK",
    "Reddit": "USA",
    "Restaurant Depot": "USA",
    "RockYou!": "USA",
    "Rosen Hotels": "USA",
    "Sakai City, Japan": "Japan",
    "San Francisco Public Utilities Commission": "USA",
    "Scottrade": "USA",
    "Scribd": "USA",
    "Seacoast Radiology, PA": "USA",
    "Sega": "Japan",
    "Service Personnel and Veterans Agency (UK)": "UK",
    "ShopBack": "Singapore",
    "SingHealth": "Singapore",
    "Slack": "USA",
    "SlickWraps": "USA",
    "SnapChat": "USA",
    "SolarWinds": "USA",
    "Sony Online Entertainment": "USA",
    "Sony Pictures": "USA",
    "Sony PlayStation Network": "Japan",
    "South Africa police": "South Africa",
    "South Carolina Government": "USA",
    "South Shore Hospital, Massachusetts": "USA",
    "Southern California Medical-Legal Consultants": "USA",
    "Spartanburg Regional Healthcare System": "USA",
    "Stanford University": "USA",
    "Starbucks": "USA",
    "Starwoodincluding Westin Hotels & Resorts and Sheraton Hotels and Resorts": "USA",
    "State of Texas": "USA",
    "Steam": "USA",
    "StockX": "USA",
    "Stratfor": "USA",
    "Supervalu": "USA",
    "Sutter Medical Center": "USA",
    "Syrian government (Syria Files)": "Syria",
    "Taobao": "China",
    "Taringa!": "Argentina",
    "Target Corporation": "USA",
    "TaxSlayer.com": "USA",
    "TD Ameritrade": "USA",
    "TD Bank": "USA",
    "TerraCom & YourTel": "USA",
    "Tetrad": "Russia",
    "Texas Lottery": "USA",
    "The Bank of New York Mellon": "USA",
    "Tianya Club": "China",
    "Ticketfly (subsidiary of Eventbrite)": "USA",
    "TikTok": "China",
    "TK / TJ Maxx": "USA",
    "T-Mobile, Deutsche Telekom": "Germany",
    "T-Mobile": "USA",
    "Tricare": "USA",
    "Triple-S Salud, Inc.": "Puerto Rico",
    "Truecaller": "Sweden",
    "Trump Hotels": "USA",
    "Tumblr": "USA",
    "Twitch": "USA",
    "Twitter": "USA",
    "Typeform": "Spain",
    "Uber": "USA",
    "Ubisoft": "France",
    "Ubuntu": "UK",
    "UCLA Medical Center, Santa Monica": "USA",
    "UK Home Office": "UK",
    "UK Ministry of Defence": "UK",
    "UK Revenue & Customs": "UK",
    "Universiti Teknologi MARA": "Malaysia",
    "Under Armour": "USA",
    "University of California, Berkeley": "USA",
    "University of Maryland, College Park": "USA",
    "University of Central Florida": "USA",
    "University of Miami": "USA",
    "University of Utah Hospital & Clinics": "USA",
    "University of Wisconsin–Milwaukee": "USA",
    "United States Postal Service": "USA",
    "UPS": "USA",
    "U.S. Army": "USA",
    "U.S. Army(classified Iraq War documents)": "USA",
    "U.S. Department of Defense": "USA",
    "U.S. Department of Veteran Affairs": "USA",
    "U.S. federal government (2020 United States federal government data breach)": "USA",
    "U.S. law enforcement (70 different agencies)": "USA",
    "National Archives and Records Administration (U.S. military veterans records)": "USA",
    "U.S. government (United States diplomatic cables leak)": "USA",
    "National Guard of the United States": "USA",
    "Vastaamo": "Finland",
    "Verizon Communications": "USA",
    "View Media": "USA",
    "Virgin Media": "UK",
    "Virginia Department of Health": "USA",
    "Virginia Prescription Monitoring Program": "USA",
    "Vodafone": "UK",
    "VTech": "Hong Kong",
    "Walmart": "USA",
    "Washington Post": "USA",
    "Washington State court system": "USA",
    "Wattpad": "Canada",
    "Wawa (company)": "USA",
    "Weebly": "USA",
    "Wendy's": "USA",
    "Westpac": "Australia",
    "Woodruff Arts Center": "USA",
    "WordPress": "USA",
    "Writerspace.com": "USA",
    "Xat.com": "USA",
    "Yahoo": "USA",
    "Yahoo Japan": "Japan",
    "Yahoo! Voices": "USA",
    "Yale University": "USA",
    "YouTube": "USA",
    "Zappos": "USA",
    "Zynga": "USA",
    "Unknown agency(believed to be tied to United States Census Bureau)": "USA",
    "National Health Information Center (NCZI) of Slovakia": "Slovakia",
    "IKEA": "Netherlands"
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
    if pd.isna(val) or val == "Unknown":
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
            'Bahrain', 'Yemen', 'Iran', 'Turkey', 'Cambodia', 'Syria'
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
    if pd.isna(val) or val == "Unknown":
        return "Unknown"
    
    val_clean = str(val).strip()
    
    # Define Welfare Sets (Based on World Bank Income Groups)
    welfare_groups = {
        "High Income": {
            'USA', 'United States', 'UK', 'United Kingdom', 'Germany', 'France', 'Japan', 
            'Canada', 'Australia', 'Sweden', 'Singapore', 'Switzerland', 'Norway', 
            'South Korea', 'UAE', 'Saudi Arabia', 'Israel', 'Qatar', 'Netherlands', 
            'Belgium', 'Austria', 'Finland', 'Ireland', 'New Zealand', 'Italy', 'Spain', 
            'Malta', 'Cyprus', 'Lithuania', 'Slovakia', 'Puerto Rico', 'Hong Kong', 
            'Chile', 'Greece', 'Taiwan', 'Denmark', 'Luxembourg', 'Iceland'
        },
        "Upper-Middle Income": {
            'China', 'Brazil', 'Russia', 'Mexico', 'Turkey', 'Argentina', 'South Africa', 
            'Thailand', 'Malaysia', 'Serbia', 'Romania', 'Bulgaria', 'Costa Rica', 
            'Panama', 'Mauritius'
        },
        "Lower-Middle Income": {
            'India', 'Indonesia', 'Vietnam', 'Philippines', 'Ukraine', 'Pakistan', 
            'Egypt', 'Nigeria', 'Uzbekistan', 'El Salvador', 'Morocco', 'Iran', 
            'Palestine', 'Bangladesh', 'Kenya', 'Cambodia'
        },
        "Low Income": {
            'Ethiopia', 'Uganda', 'Tanzania', 'Afghanistan', 'Yemen', 'Zimbabwe', 
            'Mali', 'Niger', 'Syria', 'Sudan', 'Mozambique', 'North Korea'
        }
    }

    # Direct match check
    for group, countries in welfare_groups.items():
        if val_clean in countries:
            return group
            
    return "Other/Unknown"
    
def categorize_west_or_est_country(val):
    if pd.isna(val) or val == "Unknown":
        return "Unknown"
    
    val_clean = str(val).strip()
    
    alignment_groups = {
        "Western": {
            'USA', 'United States', 'Canada', 'UK', 'United Kingdom', 'Germany', 'France', 
            'Italy', 'Spain', 'Australia', 'New Zealand', 'Netherlands', 'Sweden', 
            'Norway', 'Finland', 'Switzerland', 'Ireland', 'Malta', 'Cyprus', 'Greece', 
            'Lithuania', 'Slovakia', 'Bulgaria', 'Puerto Rico', 'Israel', 'Austria', 
            'Belgium', 'Denmark', 'Iceland', 'Luxembourg', 'Portugal', 'Czech Republic', 
            'Estonia', 'Latvia', 'Romania', 'Slovenia', 'Croatia'
        },
        "Eastern": {
            'China', 'Japan', 'South Korea', 'India', 'Russia', 'Vietnam', 'Thailand', 
            'Malaysia', 'Philippines', 'Singapore', 'Hong Kong', 'Taiwan', 'Indonesia', 
            'Pakistan', 'Iran', 'Syria', 'North Korea', 'Mongolia', 'Cambodia', 
            'Laos', 'Myanmar', 'Bangladesh', 'Sri Lanka', 'Saudi Arabia', 'UAE', 
            'Qatar', 'Turkey' 
        }
    }

    # Direct match check
    for group, countries in alignment_groups.items():
        if val_clean in countries:
            return group
            
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