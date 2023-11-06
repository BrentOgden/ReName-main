import itertools
import re
import pandas as pd
from collections import defaultdict
import os
from pathlib import Path
import chardet


# Directory where the txt files are located
dir_path = Path('files') / 'export' / 'output' / 'postingest'

# List to store dataframes for each file
dfs = []

# Iterate over each txt file in the directory
for filename in os.listdir(dir_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(dir_path, filename)
        
        # Read the content of the file
        with open(file_path, "rt") as file:
            file_content = file.read()
        
        # Split the content into lines
        lines = file_content.split("\n")
        
        # Split the lines into paragraphs based on empty lines
        paragraphs = [list(group) for key, group in itertools.groupby(lines, bool) if key]
        
        # Extract entities and their associated text for each paragraph
        paragraph_features = []
        
        for paragraph in paragraphs:
            # Initialize a dictionary to store entity texts for this paragraph
            entity_texts = defaultdict(list)
            for line in paragraph:
                # Extract entities and their types using regex
                match = re.search(r'\(([^)]+)\)', line)
                if match:
                    entity_type = match.group(1)
                    text = line.replace(f"({entity_type})", "").strip()
                    entity_texts[entity_type].append(text)
            paragraph_features.append(entity_texts)
        
        # Convert list of dictionaries to a DataFrame
        df_features = pd.DataFrame(paragraph_features)
        
        # Append dataframe to the list
        dfs.append(df_features)

# Combine all dataframes
combined_df = pd.concat(dfs, ignore_index=True)

# Export the combined dataframe to a CSV file
csv_filename = Path('files') / 'output' / 'extracted_entities.csv'
combined_df.to_csv(csv_filename, index=False)

print(f"Data exported to {csv_filename}")
print(combined_df)
