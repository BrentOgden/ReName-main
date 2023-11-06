##This script takes a set of sample data that the model has not seen and outputs the discrepancies between what the model predicted and what the true annotation ended up being.

import os
import spacy
import ast
from pathlib import Path

# Load the trained model
nlp = spacy.load(Path('files') / 'models')
# Load the data directly from the formatted_data.txt file
with open("formatted_data.txt", "rt") as file:
    TEST_DATA = [ast.literal_eval(line.strip()) for line in file.readlines()]
# Assuming TEST_DATA is a list of tuples with the format (text, annotations)
errors = []

for text, true_annotations in TEST_DATA:
    doc = nlp(text)
    predicted_entities = [(ent.text, ent.label_) for ent in doc.ents]
    true_entities = [(text[start:end], label) for start, end, label in true_annotations['entities']]
    
    if set(predicted_entities) != set(true_entities):
        errors.append({
            'text': text,
            'predicted': predicted_entities,
            'true': true_entities
        })

# Now, errors contains instances where the model's predictions did not match the true annotations
for error in errors:
    print(f"Text: {error['text']}\nPredicted: {error['predicted']}\nTrue: {error['true']}\n{'-'*50}\n")
