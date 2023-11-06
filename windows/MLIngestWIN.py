##This script should be run after the exportText.py script and will pull the output text file so that it can be NER tagged. The result of this export will then be combined into a large learning text file.

import os
import spacy

# Load the English language model
nlp = spacy.load('en_core_web_trf')

# Specify the directory path
directory_path = r'C:\Users\brandon.ainsworth\Desktop\justicia\files\export\output'

#Initialize a list to store extracted text
all_entities = []

# Iterate through all files in the directory
for filename in os.listdir(directory_path):
    # Check if the file has a .txt extension
    if filename.endswith('.txt'):
        file_path = os.path.join(directory_path, filename)
        
        # Read the content of the file
        with open(file_path, 'r') as file:
            text = file.read()
        
        # Process the text
        doc = nlp(text)
        
        for ent in doc.ents:
            all_entities.append(f"{ent.text} ({ent.label_})")

        
        # Create a new output filename
        new_output_path = r'C:\Users\brandon.ainsworth\Desktop\justicia\files\export\output\postingest'
        output_filename = "compiled_output.txt"
        output_path = os.path.join(new_output_path, output_filename)

        # # Access the tokens and print their text, POS tag, and named entity label
        # for token in doc:
        #     print(token.text, token.pos_, token.ent_type_) 
            
        # Write the results to the new file
        with open(output_path, 'w') as output_file:
            for line in all_entities:
                output_file.write(line +'\n')
