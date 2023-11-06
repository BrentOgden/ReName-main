import spacy
import os
from pathlib import Path
import chardet

# Load your trained model
nlp = spacy.load(Path('files') / 'models')

# Directory containing the files you want to process
directory_path = Path('files') / 'export' / 'output'

# Path to the output file where results will be saved
output_file_path = Path('files') / 'export' / 'output' / 'entities' / 'output.txt'

# Ensure the output directory exists
output_file_path.parent.mkdir(parents=True, exist_ok=True)

# Open the output file in write mode
with open(output_file_path, 'wt') as out_file:
    # Iterate over each file in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        # Ensure the item is a file before processing
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                result = chardet.detect(f.read())
                file_encoding = result['encoding']

            with open(file_path, 'rt', encoding=file_encoding) as f:
                for line in f:
                    doc = nlp(line.strip())  # Process each line
                    out_file.write(f"Entities in {filename} line:\n")
                    for ent in doc.ents:
                        out_file.write(f"{ent.text} - {ent.label_}\n")
                    out_file.write("-" * 50 + "\n")  # separator for clarity
