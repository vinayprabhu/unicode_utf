import requests
import pandas as pd
import io
import requests

def get_unicode_scripts_df():
    url = "https://www.unicode.org/Public/17.0.0/ucd/Scripts.txt"
    response = requests.get(url)
    response.raise_for_status()
    
    rows = []
    for line in response.text.splitlines():
        # Skip empty lines and header comments
        if not line.strip() or line.startswith('#'):
            continue
        
        # Split data from the comment section
        # Example: 0000..001F ; Common # Cc [32] <control-0000>..<control-001F>
        data_part, comment_part = line.split('#', 1)
        
        # Parse Code Range and Script Name
        range_hex, script = [x.strip() for x in data_part.split(';')]
        
        # Parse General Category and Notes
        comment_tokens = comment_part.strip().split()
        gen_cat = comment_tokens[0]
        
        # Skip the repetition count [n] if it exists
        if len(comment_tokens) > 1 and comment_tokens[1].startswith('['):
            notes = " ".join(comment_tokens[2:])
        else:
            notes = " ".join(comment_tokens[1:])
            
        # Unwrap ranges into individual code points
        if '..' in range_hex:
            start_str, end_str = range_hex.split('..')
            start, end = int(start_str, 16), int(end_str, 16)
        else:
            start = end = int(range_hex, 16)
            
        for cp in range(start, end + 1):
            rows.append({
                "codepoint_hex": f"{cp:04X}",
                "script": script,
                "general_category": gen_cat,
                "notes_or_range": notes
            })
            
    return pd.DataFrame(rows)

# Generate the dataframe
df = get_unicode_scripts_df()
df.to_csv('df_unicode17_scripts.tsv',index=False,sep='\t')

def get_iso_15924_table():
    url = "https://unicode.org/iso15924/iso15924-codes.html"
    
    # Use a header to mimic a browser
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    # Parse the HTML tables
    tables = pd.read_html(response.text)
    
    # We want the table that contains the actual script data
    # Usually the first large table on the page
    df = None
    for t in tables:
        # Check if "Code" and "N°" are in the columns to identify the right table
        if any(col in str(t.columns) for col in ["Code", "N°"]):
            df = t
            break
            
    if df is None:
        raise ValueError("Target ISO 15924 table not found on page.")

    # Clean the column names: convert to string first, then strip
    df.columns = [str(col).strip() for col in df.columns]
    
    # Drop rows that might be sub-headers or empty (if any)
    df = df.dropna(subset=['Code', 'N°'])
    
    return df

# Generate and save
try:
    iso_df = get_iso_15924_table()
    
    # Save to TSV
    iso_df.to_csv("df_iso15924_scripts.tsv", sep='\t', index=False)
    
    print("DataFrame generated successfully!")
    print(iso_df.head(10))
except Exception as e:
    print(f"An error occurred: {e}")
