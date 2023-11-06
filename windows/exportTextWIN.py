import os
import re
from pdf2image import convert_from_path
import pytesseract
import nltk
from pathlib import Path

directory_path = Path('files') / 'export'  # Path to the directory containing the PDF files
output_directory = Path('files') / 'export' / 'output'  # Path to the directory where the results will be saved

# Ensure the output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Iterate over each file in the directory
for filename in os.listdir(directory_path):
    # Check if the file is a PDF
    if filename.endswith('.pdf'):
        file_path = os.path.join(directory_path, filename)

        # Convert each page of the PDF to an image
        pages = convert_from_path(file_path)

        # Process only the first page
        page = pages[0]

        # Extract the text from the page image
        text = pytesseract.image_to_string(page)

        # Split the text into sentences
        sentences = nltk.sent_tokenize(text)

        # Join the sentences into a single string
        text = ' '.join(sentences)

        # Use regex to capture the 8 words before the opening parentheses
        # matches = re.findall(r'((?:\S+\s+){8})\(', text)

        # Create the output text file name based on the PDF file name
        output_filename = os.path.join(output_directory, filename.replace('.pdf', '.txt'))

        # Write the results to the output text file
        with open(output_filename, 'w') as output_file:
            output_file.write(f"Processing file: {filename}\n")
            output_file.write(text + "\n\n")
            # for match in matches:
            #     output_file.write(f"8 words before opening parentheses are: '{match}'\n")
            output_file.write("-------------------------------------------------------\n")