import os
from pathlib import Path
from datetime import datetime
import re

# Path to the directory containing different folders with PDF files
main_file_path = Path('files') / 'export'

# Path to the TXT files containing the entity values
text_files_path = Path('files') / 'export' / 'output' / 'entities'

def read_entity_values_from_file(file_path):
    with open(file_path, 'rt') as file:
        entity_values = {"VENDOR": [], "TYPE": [], "DATE": []}
        for line in file.readlines(): 
            if '-' not in line:
                continue
            entity_value, entity_type = line.rsplit('-', 1)
            entity_type = entity_type.strip()
            entity_value = entity_value.strip()
            if entity_type == 'TYPE':
                entity_value = re.sub(r'^\b(of|in|on|for|the|this)\b\s*', '', entity_value, flags=re.IGNORECASE) 
            if entity_type in entity_values:
                entity_values[entity_type].append(entity_value)
        
        first_entity_values = {k: select_most_appropriate_value(v) for k, v in entity_values.items()}
    return first_entity_values

def select_most_appropriate_value(values):
    for value in values:
        if value:
            for date_format in ['%B %d, %Y', '%B, %Y', '%B %Y']:
                try:
                    datetime.strptime(value, date_format)
                    return value
                except ValueError:
                    continue
            return value
    return None

def rename_pdf(pdf_file_path, entity_values, parent_folder_name):
    pdf_file_stem = pdf_file_path.stem
    if entity_values.get('DATE'):
        valid_date_found = False
        try:
            for date_format in ['%B %d, %Y', '%B, %Y', '%B %Y']:
                try:
                    formatted_date = datetime.strptime(entity_values['DATE'], date_format).strftime('%m-%d-%y')
                    entity_values['DATE'] = formatted_date
                    valid_date_found = True
                    break
                except ValueError:
                    continue
        except ValueError:
            pass
        
        if not valid_date_found:
            entity_values['DATE'] = None
                
    new_file_name_entities = [
        entity_values.get('VENDOR'),
        entity_values.get('TYPE'),
        parent_folder_name,
        entity_values.get('DATE')
    ]
    
    new_file_name = '_'.join(filter(None, new_file_name_entities))
    abs_path = os.path.abspath(pdf_file_path)
    directory, filename = os.path.split(abs_path)
    base, extension = os.path.splitext(filename)
    os.rename(abs_path, os.path.join(directory, new_file_name + extension))

# Check each folder in the root directory and find the matching TXT file for each PDF to get the entity values
for folder in main_file_path.iterdir():
    if folder.is_dir():
        for pdf_file_path in folder.rglob('*.pdf'):
            try:  # Add a try block here
                pdf_file_stem = pdf_file_path.stem
                txt_file_name = f"results_{pdf_file_stem}.txt"
                txt_file_path = text_files_path / txt_file_name
                if txt_file_path.exists():
                    entity_values = read_entity_values_from_file(txt_file_path)
                    parent_folder_name = folder.name
                    rename_pdf(pdf_file_path, entity_values, parent_folder_name)
                else:
                    print(f"No matching TXT file found for PDF: {pdf_file_path}")  # Inform the user about the missing TXT file
            except Exception as e:  # Catch any other exceptions that might occur
                print(f"An error occurred while processing PDF file {pdf_file_path}: {e}")
