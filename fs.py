import pandas as pd

df = pd.read_csv("output.csv")

import re

# 1. Define a function to extract all quoted terms from the malformed string
def extract_terms(text):
    if pd.isna(text):
        return []
    # This regex finds everything inside '...' or "..."
    return re.findall(r"['\"](.*?)['\"]", str(text))

# 2. Apply it to your column to turn the strings into proper Python lists
df['artist_terms_clean'] = df['artist_terms'].apply(extract_terms)

# 3. Flatten the clean lists and extract all unique values
unique_values = df['artist_terms_clean'].explode().dropna().unique()

# 4. Optional: Remove any blank empty strings caused by double quotes (like "")
unique_values = [term for term in unique_values if term.strip()]

print(unique_values)

# 1. Assuming 'unique_values' is your list of terms from the previous step:
# Sort by length descending so longer phrases match before shorter sub-words
unique_values.sort(key=len, reverse=True)

# 2. Escape special characters and join with '|' (OR operator)
# \b ensures it matches whole phrases/words, not just pieces of words
pattern = r'\b(' + '|'.join(map(re.escape, unique_values)) + r')\b'

print(pattern)