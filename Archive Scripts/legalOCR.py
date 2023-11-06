from pdf2image import convert_from_path
import pytesseract


pages = convert_from_path('files/CleanChoice_MSA_(Dish_Execution_Version_2.25.22)_fe.pdf')


for i, page in enumerate(pages):
    text = pytesseract.image_to_string(page)
    with open(f'output_page_{i}.txt', 'w') as file:
        file.write(text)
        print(text)

specific_texts = ['Agreement', 'Vendor', 'Effective Date', 'DISH']  # replace with your specific texts


found_texts = {text: False for text in specific_texts}

with open('output_page_0.txt', 'r') as file:
    for line in file:
        for specific_text in specific_texts:
            if specific_text in line and not found_texts[specific_text]:
                print(f"First instance of '{specific_text}' found in line: {line}")
                found_texts[specific_text] = True
        if all(found_texts.values()):  # if all texts have been found, break the loop
            break

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