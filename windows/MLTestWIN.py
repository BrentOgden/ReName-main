import os
import spacy

# Load the English language model
nlp = spacy.load('en_core_web_trf')

# Specify the directory path
directory_path = 'files/output'

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
        
        # Create a new output filename
        output_filename = os.path.splitext(filename)[0] + "_output.txt"
        output_path = os.path.join(directory_path, output_filename)

        # Access the tokens and print their text, POS tag, and named entity label
        for token in doc:
            print(token.text, token.pos_, token.ent_type_) 
            
        # Write the results to the new file
        with open(output_path, 'w') as output_file:
            for token in doc:
                output_line = f"{token.text} {token.pos_} {token.ent_type_}\n"
                output_file.write(output_line)
