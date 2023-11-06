import os
import spacy

# Load the trained model
nlp = spacy.load(r"C:\Users\brandon.ainsworth\Desktop\justicia\files\models")

# Directory containing the test files
test_files_directory = r"C:\Users\brandon.ainsworth\Desktop\justicia\files\train\output"
result_files_directory = r"C:\Users\brandon.ainsworth\Desktop\justicia\files\train\output\trainoutput"

# Iterate over each file in the test directory
for filename in os.listdir(test_files_directory):
    if filename.endswith('.txt'):  # Check if the file is a text file
        file_path = os.path.join(test_files_directory, filename)

        # Read the content of the current file for testing
        with open(file_path, "r") as file:
            test_text = file.read()

        # Use the model to predict entities in the test text
        doc = nlp(test_text)

        # Name of the output file based on the input file name
        output_filename = f"results_{filename}"
        output_path = os.path.join(result_files_directory, output_filename)

        # Save the results to a .txt file
        with open(output_path, "w") as out_file:
            for ent in doc.ents:
                out_file.write(f"{ent.text} - {ent.label_}\n")
                print(ent.text, ent.label_)
