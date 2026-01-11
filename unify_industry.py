
import pandas as pd

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
