import os
import re
import PyPDF2

# Define the path to your PDF file
file_path = 'files/DISH.pdf'

# Define the specific text (or regular expression) you want to use as the new name
new_names = ['STATEMENT OF WORK No. 1', 'DISH Purchasing Corporation', 'February 9, 2021']

def rename_pdf(file_path, new_names):
    # Open the PDF file
    with open(file_path, 'rb') as pdf_file:
        # Create a PDF file reader object
        reader = PyPDF2.PdfReader(pdf_file)

        # Get the text from the PDF file
        text = ''
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()

        # Initialize new file name
        new_file_name = ''

        # Find the specific text for each name in new_names
        for new_name in new_names:
            match = re.search(new_name, text)

            if match:
                new_file_name += new_name + '_'

        if new_file_name:
            # Remove the trailing underscore
            new_file_name = new_file_name.rstrip('_')

            # Get the absolute path of the file
            abs_path = os.path.abspath(file_path)
            # Get the directory and the base filename
            directory, filename = os.path.split(abs_path)
            # Split the base filename to get the extension
            base, extension = os.path.splitext(filename)

            # Rename the file
            os.rename(abs_path, os.path.join(directory, new_file_name + extension))

# Call the function
rename_pdf(file_path, new_names)
