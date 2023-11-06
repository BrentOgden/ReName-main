# import re
# from pdf2image import convert_from_path
# import pytesseract
# import nltk

# # Convert each page of the PDF to an image
# pages = convert_from_path('files/Aero-DWRP_MPA_09.15.22.pdf')

# # Process only the first page
# page = pages[0]

# # Extract the text from the page image
# text = pytesseract.image_to_string(page)

# # Split the text into sentences
# sentences = nltk.sent_tokenize(text)

# # Initialize the first paragraph as an empty string
# first_paragraph = ""

# # Process each sentence
# for sentence in sentences:
#     # If the sentence starts with "This", start the first paragraph
#     if sentence.startswith("This"):
#         first_paragraph = sentence
#         break

# # Define the specific texts to search for
# # specific_texts = ['Agreement', 'Vendor', 'Effective Date', 'DISH']

# # Use regex to capture the 30 words before the opening parentheses
# matches = re.findall(r'((?:\S+\s+){30})\(', first_paragraph)
# for match in matches:
#     print(f"30 words before opening parentheses are: '{match}'")

#     # Search for the specific texts within the match
#     # for specific_text in specific_texts:
#     #     if specific_text in match:
#     #         print(f"'{specific_text}' found in the 30 words before opening parentheses.")






# import re
# from pdf2image import convert_from_path
# import pytesseract
# import nltk

# # Convert each page of the PDF to an image
# pages = convert_from_path('files/Aero-DWRP_MPA_09.15.22.pdf')

# # Process only the first page
# page = pages[0]

# # Extract the text from the page image
# text = pytesseract.image_to_string(page)
# print(text)

# # Split the text into sentences
# sentences = nltk.sent_tokenize(text)

# # Join the sentences into a single string
# text = ' '.join(sentences)

# # Define the specific texts to search for
# specific_texts = ['Agreement', 'Vendor', 'Effective Date', 'DISH']

# # Use regex to capture the 30 words before the opening parentheses
# matches = re.findall(r'((?:\S+\s+){30})\(', text)
# for match in matches:
#     print(f"30 words before opening parentheses are: '{match}'")

#     # Search for the specific texts within the match
#     for specific_text in specific_texts:
#         if specific_text in match:
#             print(f"'{specific_text}' found in the 30 words before opening parentheses.")




############This is a block of code that will pull the 25 words prior to the first 4 occurences of an opening parentheses - it allows for the first instance to have less than 25 words prior to the parentheses

import re
from pdf2image import convert_from_path
import pytesseract
import pandas as pd
import nltk
import os
import glob

# Path to the directory
dir_path = 'files/test'

# Output directory
output_dir = 'files/test/output/'

# Make sure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Get a list of all PDF files in the directory and subdirectories
pdf_files = glob.glob(dir_path + '**/*.pdf', recursive=True)

# Create a list of dictionaries representing the data
data = []

for file in pdf_files:

    # Convert each page of the PDF to an image
    pages = convert_from_path(file)

    # Process only the first page
    page = pages[0]

    # Extract the text from the page image
    text = pytesseract.image_to_string(page)

    # Split the text into sentences
    sentences = nltk.sent_tokenize(text)

    # Join the sentences into a single string
    text = ' '.join(sentences)

    # Use regex to capture up to 25 words before the opening parentheses
    # matches = re.findall(r'((?:\S+\s+){0,25})\(', text)

    # Open the .txt file for writing
    with open(os.path.join(output_dir, os.path.basename(file) + '.txt'), 'w') as f:

        # Process only the first 4 matches
        # for i, match in enumerate(matches):
        #     if i >= 4:  # Stop after the 4th match
        #         break
        #     # print(f"Up to 25 words before occurrence #{i+1} of opening parentheses are: '{match}'")
        #     # f.write(f"Up to 25 words before occurrence #{i+1} of opening parentheses are: '{match}'\n")
        #     print({match})
        #     f.write(f"#{i+1} : '{match}'\n")
            data.append({"File": os.path.basename(file), "Occurrence": i+1, "Words": match})

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Export the DataFrame to a CSV file
df.to_csv("files/output/words_before_parentheses.csv", index=False)


###################





# from pdf2image import convert_from_path
# import pytesseract

# # Convert each page of the PDF to an image
# pages = convert_from_path('files/Aero-DWRP_MPA_09.15.22.pdf')

# for i, page in enumerate(pages):
#     text = pytesseract.image_to_string(page)
#     with open(f'output_page_{i}.txt', 'w') as file:
#         file.write(text)
#         print(text)

# # Define the specific texts to search for
# specific_texts = ['ÄúAgreementÄú', 'ÄúVendorÄú', 'ÄúEffective DateÄú', 'ÄúDISHÄú']
# found_texts = {text: False for text in specific_texts}

# # Process each page
# for i, page in enumerate(pages):
#     # Extract the text from the page image
#     text = pytesseract.image_to_string(page)

#     # Split the text into lines
#     lines = text.split('\n')

#     # Process each line
#     for line in lines:
#         # Check each specific text
#         for specific_text in specific_texts:
#             # If this is the first occurrence of the specific text in this line, print it
#             if specific_text in line and not found_texts[specific_text]:
#                 print(f"First instance of '{specific_text}' found in line: {line}")
#                 found_texts[specific_text] = True

#     # If all specific texts have been found, stop processing
#     if all(found_texts.values()):
#         break







# from pdf2image import convert_from_path
# import pytesseract


# pages = convert_from_path('files/Aero-DWRP_MPA_09.15.22.pdf')


# for i, page in enumerate(pages):
#     text = pytesseract.image_to_string(page)
#     with open(f'output_page_{i}.txt', 'w') as file:
#         file.write(text)
#         print(text)

# specific_texts = ['Agreement', 'Vendor', 'Effective Date', 'DISH']  # replace with your specific texts


# found_texts = {text: False for text in specific_texts}

# with open('output_page_0.txt', 'r') as file:
#     for line in file:
#         for specific_text in specific_texts:
#             if specific_text in line and not found_texts[specific_text]:
#                 print(f"First instance of '{specific_text}' found in line: {line}")
#                 found_texts[specific_text] = True
#         if all(found_texts.values()):  # if all texts have been found, break the loop
#             break

# with open('output_page_0.txt', 'r') as file:
#     for line in file:
#         for specific_text in specific_texts:
#             if specific_text in line:
#                 print(f"'{specific_text}' found in line: {line}")
# specific_texts = ['text1', 'text2', 'text3']  # replace with your specific texts
# found_texts = {text: False for text in specific_texts}

# with open('output_page_0.txt', 'r') as file:
#     prev_line = next_line = None
#     for line in file:
#         next_line = file.readline()
#         for specific_text in specific_texts:
#             if specific_text in line and not found_texts[specific_text]:
#                 print(f"Line before first instance of '{specific_text}': {prev_line}")
#                 print(f"First instance of '{specific_text}' found in line: {line}")
#                 print(f"Line after first instance of '{specific_text}': {next_line}")
#                 found_texts[specific_text] = True
#         if all(found_texts.values()):  # if all texts have been found, break the loop
#             break
#         prev_line = line

       
# with open('output_page_0.txt', 'r') as file:
#     for line in file:
#         if 'Effective Date' in line:
#             print(line)