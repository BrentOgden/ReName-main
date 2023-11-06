####
#This script takes a file consisting of all of the exported feature data from each individual file export compiled into one large file. That file is then formatted and prepared for training by separating into individual text segments and corresponding labels. It is then converted to the format used by spaCy and exported to a txt file.


import re

# Load the data from the file
with open(r"C:\Users\brandon.ainsworth\Desktop\justicia\files\export\output\postingest\compiled_output.txt", "r") as file:
    content = file.read()

# Function to convert parsed data to spaCy format
def convert_to_spacy_format(text, label):
    return (text, {"entities": [(0, len(text), label)]})

# Parse the content to separate text segments and their corresponding labels
pattern = re.compile(r"([^()]+)\s\((ORG|DATE|LAW|CARDINAL|GPE|MONEY|PERSON|.+?)\)")
matches = pattern.findall(content)

# Convert matches to spaCy training format
TRAIN_DATA = [convert_to_spacy_format(match[0].strip(), match[1]) for match in matches]

# Save the formatted data to a new file
with open(r"C:\Users\brandon.ainsworth\Desktop\justicia\formatted_data.txt", "w") as file:
    for item in TRAIN_DATA:
        file.write(str(item) + "\n")

print("Data has been formatted and saved to 'formatted_data.txt'")
