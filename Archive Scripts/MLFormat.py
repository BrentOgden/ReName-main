####
#This script takes a file consisting of all of the exported feature data from each individual file export compiled into one large file. That file is then formatted and prepared for training by separating into individual text segments and corresponding labels. It is then converted to the format used by spaCy and exported to a txt file.

import os
import re
from pathlib import Path

import chardet

# Load the data from the file
with open(Path('files') / 'export' / 'output' / 'postingest' / "compiled_output.txt", "rt") as file:
    content = file.read()

# Convert the values in ORG_SET to lowercase for case-insensitive comparison
ORG_SET = {org.lower() for org in ["American H Block Wireless, L.L.C.", 
           "Blockbuster, L.L.C.", 
           "CMBSat", 
           "DBSD Corporation", 
           "DISH", 
           "DISH Wireless, L.L.C.", 
           "DISH Wireless Leasing, L.L.C.", 
           "DISH Wireless Retail Purchasing, L.L.C.", 
           "DNCSC", "Dish Digital, L.L.C.", 
           "Dish Network Corporation", 
           "Dish Network, L.L.C.", 
           "Dish Network Service Corporation", 
           "Dish Network Services, L.L.C.", 
           "Dish Orbital II", 
           "Dish Purchasing Corporation",
           "DISH Purchasing Corporation", 
           "Dish Technologies", 
           "Gamma Acquisition, L.L.C.", 
           "Manifest Wireless, L.L.C.", 
           "ParkerB.com, L.L.C.", 
           "Wetterhorn Wireless, L.L.C.", 
           "DISH Orbital Corporation",
           "DISH DBS Corporation",
           "DISH Network L.L.C.",
           "DISH Purchasing Corp.",
           "DISH Purchasing",
           "DISH NETWORK CORPORATION",
           "DISH Operating L.L.C.",
           "Echosphere L.L.C.",
           "Dish Network Service L.L.C.",
           "DISH Wireless Holding L.L.C.",
           "DISH Wireless L.L.C.",
           "EchoStar Broadcasting Corporation",
           "DISH Technologies L.L.C.",
           "Sling TV Holding L.L.C.",
           "Sling TV",
           "Blockbuster LLC",
           "Sling Media Inc.",
           "AirTV L.L.C.",
           "Dish Network Canada ULC",
           "Dish Mexico, S. de R.L. de C.V.",
]}


# Function to convert parsed data to spaCy format
def convert_to_spacy_format(text, label):
    # Check if the text is in ORG_SET
    if text.lower() in ORG_SET:
        label = "ORG"
    elif label == "ORG":
        label = "VENDOR"
    elif label == "LAW":
        label = "TYPE"
    return (text, {"entities": [(0, len(text), label)]})

# Parse the content to separate text segments and their corresponding labels
# Note: Added re.IGNORECASE flag for case-insensitive matching
pattern = re.compile(r"([^()]+)\s\((ORG|DATE|LAW|CARDINAL|GPE|MONEY|PERSON|TYPE|VENDOR|.+?)\)", re.IGNORECASE)
matches = pattern.findall(content)

# Convert matches to spaCy training format and adjust the label based on ORG_SET
TRAIN_DATA = [convert_to_spacy_format(match[0].strip(), match[1].upper()) for match in matches]

# Save the formatted data to a new file
with open("updated_formatted_data.txt", "wt") as file:
    for item in TRAIN_DATA:
        file.write(str(item) + "\n")


