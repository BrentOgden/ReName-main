import os
from pdf2image import convert_from_path
import pytesseract
from pathlib import Path
from docx import Document
from multiprocessing import Pool
from functools import partial

def process_file(directory_path, output_directory, filename):
    try:
        file_path = os.path.join(directory_path, filename)
        # Check if the file is a PDF
        if filename.endswith('.pdf'):
            # Get the number of pages in the PDF
            num_pages = len(convert_from_path(file_path, first_page=1, last_page=1))
            # Convert only the first and last pages to images
            pages = convert_from_path(file_path, first_page=1, last_page=num_pages)
            first_page = pages[0]
            last_page = pages[-1 if num_pages > 1 else 0]  # Handle case with single page
            # Extract the text from the first and last page images
            first_page_text = pytesseract.image_to_string(first_page).split()
            last_page_text = pytesseract.image_to_string(last_page).split()
            # Remove lines containing "processing" from the first page text
            first_page_lines = first_page_text.split('\n')
            first_page_lines = [line for line in first_page_lines if 'processing' not in line.lower()]
            first_page_text = '\n'.join(first_page_lines)
            
            output_filename = os.path.join(output_directory, filename.replace('.pdf', '.txt'))
            text = f"{first_page_text}/n/n{last_page_text}"

        elif filename.endswith('.docx'):
            doc = Document(file_path)
            paragraphs = [paragraph.text.split() for paragraph in doc.paragraphs]
            # Assuming that a page break is represented by two newline characters, 
            # this will get the text before the first page break and after the last page break
            pages = '\n'.join(paragraphs).split('\n\n')
            first_page_text = pages[0].split()
            last_page_text = pages[-1].split()
            output_filename = os.path.join(output_directory, filename.replace('.docx', '.txt'))
            
            # Remove lines containing "processing" from the first page text
            first_page_lines = first_page_text.split('\n')
            first_page_lines = [line for line in first_page_lines if 'processing' not in line.lower()]
            first_page_text = '\n'.join(first_page_lines)
            
            text = f"{first_page_text}/n/n{last_page_text}"

        else:
            return
        
        # Write the results to the output text file
        with open(output_filename, 'wt') as output_file:
            output_file.write(text + "\n\n")
            output_file.write("-------------------------------------------------------\n")

    except Exception as e:
        print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    directory_path = Path('files') / 'export'
    output_directory = Path('files') / 'export' / 'output'

    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Partially apply the process_file function to create a new function with directory_path and output_directory pre-filled
    process_file_with_paths = partial(process_file, directory_path, output_directory)

    # Create a pool of worker processes
    with Pool() as pool:
        pool.map(process_file_with_paths, os.listdir(directory_path))
