import os
import spacy
from pathlib import Path
import re

# Load the English language model
nlp = spacy.load('en_core_web_trf')

# Specify the directory path
directory_path = Path('files') / 'export' / 'output'

# Desired entities set
desired_entities = {"ORG", "DATE", "LAW", "VENDOR", "TYPE"}

# Initialize a list to store extracted text
all_entities = []

# Precompile regex patterns
date_line_pattern = re.compile(r'\b(\d{1,2}|\d{4}|January|February|March|April|May|June|July|August|September|October|November|December|DATE)\b', re.IGNORECASE)
parentheses_pattern = re.compile(r'\([^)]*\)')
quotes_pattern = re.compile(r'"[^"]*"')


def merge_date_lines(text):
    lines = text.split('\n')
    
    i = 0
    while i < len(lines) - 1:
        current_line = lines[i].strip()
        next_line = lines[i + 1].strip()
        
      # If the current line ends with a potential date component and so does the next line, merge them
        if date_line_pattern.search(current_line.split()[-1]) and date_line_pattern.search(next_line.split()[-1]):
            lines[i] = current_line + " " + next_line + "\n"
            del lines[i + 1]
        else:
            i += 1

    return '\n'.join(lines)

def remove_text_inside_parentheses_and_quotes(text):
    text = parentheses_pattern.sub('', text)  # Remove text inside parentheses
    text = quotes_pattern.sub('', text)       # Remove text inside quotes
    return text

# Iterate through all files in the directory with .txt extension
for file_path in directory_path.glob('*.txt'):
    # Read the content of the file
    with open(file_path, 'rt') as file:
        text = file.read()
        
    # Remove text inside closed parentheses
    text = remove_text_inside_parentheses_and_quotes(text)
        
    # Process the text with spaCy
    doc = nlp(text)
        
    for ent in doc.ents:
        if ent.label_ in desired_entities:
            all_entities.append(f"{ent.text} ({ent.label_})")

   # Create a new output directory and filename
    new_output_path = Path('files') / 'export' / 'output' / 'postingest' 
    output_filename = "compiled_output.txt"
    output_path = new_output_path / output_filename

    # Ensure the output directory exists
    new_output_path.mkdir(parents=True, exist_ok=True)

    # Write the desired entities to the new file
    with open(output_path, 'wt') as output_file:
        output_file.write('\n'.join(all_entities))
