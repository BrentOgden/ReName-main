import os
import spacy
from spacy.tokens import Doc
from spacy.training import Example
from spacy.util import minibatch, compounding 
import ast
from pathlib import Path
import random
import chardet
import re

nlp = spacy.load("en_core_web_trf")

# Load the data directly from the updated_formatted_data.txt file using regex
with open("updated_formatted_data.txt", "rt") as file:
    content = file.read()
    matches = re.findall(r"\('(.*?)', \{'entities': \[(.*?)\]\}\)", content)
    structured_data_regex = [
        (match[0], {"entities": [(int(tup[0]), int(tup[1]), tup[2]) for tup in re.findall(r"\((\d+), (\d+), '(.*?)'\)", match[1])]})
        for match in matches
    ]

# Split the data into training and validation sets (e.g., 80% train, 20% validation)
split_point = int(0.8 * len(structured_data_regex))
TRAIN_DATA = structured_data_regex[:split_point]
VALID_DATA = structured_data_regex[split_point:]

ner = nlp.get_pipe('ner')
custom_labels = ["TYPE", "VENDOR"]
for label in custom_labels:
    ner.add_label(label)

# Add the entity labels to the NER model
for _, annotations in TRAIN_DATA:
    for ent in annotations.get("entities"):
        ner.add_label(ent[2])

# Train the model with modified hyperparameters
optimizer = nlp.resume_training()

for itn in range(2):  # Adjusting the number of iterations
    random.shuffle(TRAIN_DATA)
    for text, annotations in TRAIN_DATA:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        nlp.update([example], drop=0.2, sgd=optimizer)  # Adjusting the dropout rate

    # Simple evaluation using the validation data
    correct_predictions = 0
    for text, annotations in VALID_DATA:
        doc = nlp(text)
        entities = [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
        if entities == annotations["entities"]:
            correct_predictions += 1
    accuracy = correct_predictions / len(VALID_DATA)
    print(f"Iteration {itn + 1}: Validation Accuracy: {accuracy * 100:.2f}%")

# Save the model to a directory
nlp.to_disk(Path('files') / 'models')
