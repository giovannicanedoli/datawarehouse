
import pandas as pd
df1 = pd.read_csv("organization_data_breaches.csv")
df2 = pd.read_csv("Global_Cybersecurity_Threats_2015-2024.csv")
df3 = pd.read_csv("LossFromNetCrime.csv")

print(set(df2["Country"]))

#convert df3[country] using the following map
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

df3['Country'] = df3['Country'].map(country_map)




#idea one: uniform df_1 nation id with global_cybersecurity_threats
#idea two: cybersecurity threats narrows from 2015, the other datasets have different time ranges!