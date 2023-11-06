
from datetime import datetime
from docx import Document
from functools import partial
from multiprocessing import Pool
from pathlib import Path
import PyPDF2
from pdf2image import convert_from_path
from dateutil import parser
from os import walk
import os
import pytesseract
import re
import spacy
from concurrent.futures import ProcessPoolExecutor


input_directory = Path('files') / 'export'
output_directory = Path('files') / 'export' / 'output'
# directory_path = Path('files') / 'export'
# output_directory = Path('files') / 'export' / 'output'

# Load the English language model for spaCy
nlp_ingest = spacy.load('en_core_web_trf')

# Load your trained model
nlp = spacy.load(Path('files') / 'models')

# Define ORG_SET and TYPE_SET
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
           ]}  # Set of organization names
TYPE_SET = {type.lower() for type in ["Statement of Work",
             "Master Services Agreement",
             "Non-Disclosure Agreement",
             "Amendment to Master Purchasing Agreement",
             "Lease Agreement",
             "Employment Contract",
             "Licensing Agreement",
             "Franchise Agreement",
             "Loan Agreement",
             "Real Estate Purchase Agreement",
             "Software Licensing Agreement",
             "Supply Agreement",
             "Distribution Agreement",
             "Vendor Agreement",
             "Sales Agreement",
             "Memorandum of Understanding",
             "Renewal Notice",
             "Order Form",
             "Accessory Agreement",
             "Retailer Agreement",
             "Procurement Agreement",
             "Software License Agreement",
             "Joinder",
             "Price Quote",
             "Client Authorization",
             "Consulting Services Agreement",
             "Sales Order Amendment",
             "Subscription Agreement",
             "Client Agreement",
             "Letter of Intent",
             "Amendment No.1",
             "Amendment No.2",
             "Amendment No.3",
             "Amendment No.4",
             "Amendment No.5",
             "Amendment No.6",
             "Amendment No.7",
             "Amendment No.8",
             "Amendment No.9",
             "Amendment No.10",
             "Amendment No.11",
             "Amendment No.12",
             "Amendment No.13",
             "Amendment No.14",
             "First Amendment",
             "Second Amendment",
             "Third Amendment",
             "Fourth Amendment",
             "Fifth Amendment",
             "Sixth Amendment",
             "Seventh Amendment",
             "Eigth Amendment",
             "Ninth Amendment",
             "Tenth Amendment",
             "Service Schedule",
             "Data Service Agreement",
             "Dealer Door Lease Agreement",
             "Name Change Amendment"
             "Dealer Door Sublease Agreement",
             "Commencement Date Letter",
             "Assignment Rider to Lease Agreement",
             "Dealer Door Lease Extenstion",
             "PO Acknowledgement",
             "Deployment Services Agreement",
             "Appendix to Amendment",
             "Enterprise Term License Agreement",
             "DISH Lease Rider",
             "Termination Notice",
             "Spectrum Leasing Agreement",
             "Service Level Agreement",
             "Operating Agreement",
             "Consulting Agreement",
             "Purchase Order",
             "Construction Contract",
             "Mergers and Acquisitions Agreement",
             "Intellectual Property Assignment Agreement",
             "Indemnity Agreement",
             "Settlement Agreement",
             "Confidentiality Agreement",
             "Waiver and Release Agreement",
             "Agency Agreement",
             "Master Subscriber Management System Agreement",
             "Pricing Addendum",
             "Addendum 1 to Statement of Work No.10",
             "Authentication Service Addendum",
             "Billing Agent Agreement",
             "Data Services Agreement",
             "Walk-In Payment Processing Services Agreement",
             "Rental Agreement",
             "Collection Services Agreement"
             "Exclusive Distributorship Agreement",
             "Subcontractor Agreement",
             "Employment Separation Agreement",
             "Investment Agreement",
             "Licensed Data Agreement"
             "Shareholder Agreement",
             "Promissory Note",
             "Option Agreement",
             "Equity Incentive Plan",
             "Non-Compete Agreement",
             "Bill of Sale",
             "Terms and Conditions",
             "Operating Lease Agreement",
             "Maintenance Agreement",
             "Collaboration Agreement",
             "Research and Development Agreement",
             "Indemnification Agreement",
             "Power of Attorney",
             "Royalty Agreement",
             "Memorandum of Understanding",
             "Settlement and Release Agreement",
             "Statement of Work #1",
             "Statement of Work No.7",
             "Statement of Work #3",
             "Amendment to Employment Contract",
             "Affiliate Agreement",
             "Software Development Agreement",
             "Marketing Services Agreement",
             "Manufacturing Agreement",
             "Promotion and Marketing Agreement",
             "Collaborative Research Agreement",
             "Product Distribution Agreement",
             "Outsourcing Agreement",
             "Agreement for Sale of Goods",
             "Trademark License Agreement",
             "Affiliation Agreement",
             "Clinical Trial Agreement",
             "Software Subscription Agreement",
             "Content License Agreement",
             "Customer Agreement",
             "Limited Liability Company Operating Agreement",
             "Managed Services Agreement",
             "Real Estate Lease Agreement",
             "Reseller Agreement",
             "Freelance Services Agreement",
             "Investor Rights Agreement",
             "Credit Agreement",
             "Loan and Security Agreement",
             "Purchase and Sale Agreement",
             "Subscription Agreement",
             "Share Purchase Agreement",
             "Stock Option Agreement",
             "Release of Claims Agreement",
             "Software Maintenance and Support Agreement",
             "Distribution and Supply Agreement",
             "Consignment Agreement",
             "Marketing and Distribution Agreement",
             "Subscription Box Agreement",
             "Collateral Agreement",
             "Software Evaluation Agreement",
             "Consultant Agreement",
             "Equity Purchase Agreement",
             "Service Agreement for Independent Contractor",
             "Content Production Agreement",
             "Software-as-a-Service Agreement",
             "Product Development Agreement",
             "Distribution and License Agreement",
             "Marketing and Promotion Agreement",
             "Agreement for Sale of Real Property",
             "Intellectual Property License Agreement",
             "Hosted Software Services Agreement",
             "Research Agreement",
             "Assignment Agreement",
             "Stock Repurchase Agreement",
             "Stock Restriction Agreement",
             "Share Vesting Agreement",
             "Escrow Agreement",
             "Mutual Termination Agreement",
             "Service Level Agreement",
             "Joint Development Agreement",
             "Sponsorship Agreement",
             "Maintenance Services Agreement",
             "Marketing Agreement",
             "Event Sponsorship Agreement",
             "Vendor Services Agreement",
             "Cooperation Agreement",
             "Software Integration Agreement",
             "Referral Agreement",
             "Affiliation Agreement",
             "Non-Solicitation Agreement",
             "Loan Modification Agreement",
             "Technical Support Agreement",
             "Release of Liability Agreement",
             "Supply Chain Agreement",
             "Outsourcing Services Agreement",
             "Production Services Agreement",
             "Intellectual Property Transfer Agreement",
             "Subscription Services Agreement",
             "Content Creation Agreement",
             "Agency Services Agreement",
             "Software Deployment Agreement",
             "Reseller Agreement",
             "Supply Chain Management Agreement",
             "Marketing Services Agreement",
             "Investment Advisory Agreement",
             "Distribution Services Agreement",
             "Creative Services Agreement",
             "Promissory Note Agreement",
             "Product Licensing Agreement",
             "Publishing Agreement",
             "Research and Development Services Agreement",
             "Royalty Payment Agreement",
             "Sublicensing Agreement",
             "Strategic Partnership Agreement",
             "Technology Transfer Agreement",
             "Territorial Licensing Agreement",
             "Trademark Assignment Agreement",
             "User Agreement",
             "Value-Added Reseller Agreement",
             "Warranty Agreement",
             "Web Hosting Agreement",
             "White Label Agreement",
             "Work for Hire Agreement",
             "Website Development Agreement",
             "Software Escrow Agreement",
             "Software Support and Maintenance Agreement",
             "Social Media Influencer Agreement",
             "Software Licensing and Distribution Agreement",
             "Master Franchise Agreement",
             "International Distribution Agreement",
             "Collaboration and Licensing Agreement",
             "Data Processing Agreement",
             "Education Services Agreement",
             "Facility Use Agreement",
             "Franchise Disclosure Document",
             "Indemnification and Hold Harmless Agreement",
             "Integration and Implementation Agreement",
             "Subscriber Agreement",
             "Service Plan Agreement",
             "Equipment Lease Agreement",
             "Terms of Service Agreement",
             "Programming Agreement",
             "Installation Agreement",
             "Service Maintenance Agreement",
             "Customer Agreement",
             "Authorized Dealer Agreement",
             "Broadcast Content Agreement",
             "Signal Distribution Agreement",
             "Content Licensing Agreement",
             "Network Distribution Agreement",
             "Retailer Agreement",
             "Authorized Installer Agreement",
             "Marketing and Promotion Agreement",
             "Technology Integration Agreement",
             "Satellite Transmission Agreement",
             "Content Delivery Agreement",
             "Channel Partner Agreement",
             "Marketing Services Agreement",
             "Advertising Agreement",
             "Digital Content Distribution Agreement",
             "Subscriber Data Protection Agreement",
             "Technical Support Services Agreement",
             "Video-on-Demand Agreement",
             "Mobile App Distribution Agreement",
             "Network Access Agreement",
             "Broadcasting Services Agreement",
             "Interactive Services Agreement",
             "Local Programming Agreement",
             "Master Service Agreement",
             "Program Distribution Agreement",
             "Distribution Rights Agreement",
             "Broadcast Syndication Agreement",
             "Video Streaming Agreement",
             "Satellite Transmission Services Agreement",
             "Technical Equipment Agreement",
             "Co-Branding Agreement",
             "Customer Support Services Agreement",
             "Content Aggregation Agreement",
             "Subscriber Data Privacy Agreement",
             "Authorized Retailer Agreement",
             "Subscriber Billing Agreement",
             "Local Channel Agreement",
             "Customer Installation Agreement",
             "Product Promotion Agreement",
             "Subscriber Authentication Agreement",
             "Network Maintenance Agreement",
             "Content Delivery Network Agreement",
             "Set-Top Box Lease Agreement",
             "Content Synchronization Agreement",
             "Technical Integration Agreement",
             "Interactive Program Agreement",
             "Broadcast Rights Agreement",
             "Broadcast Signal Transmission Agreement",
             "Satellite Uplink Agreement",
             "Local Advertising Agreement",
             "Settlement Agreement",
             "Litigation Services Agreement",
             "Legal Representation Agreement",
             "Dispute Resolution Agreement",
             "Mediation Agreement",
             "Arbitration Agreement",
             "Negotiation Services Agreement",
             "Confidentiality Agreement",
             "Non-Disclosure Agreement",
             "Release and Waiver Agreement",
             "Consent Decree",
             "Joint Defense Agreement",
             "Expert Witness Agreement",
             "Legal Services Retainer Agreement",
             "Counseling Services Agreement",
             "Pretrial Stipulation Agreement",
             "Litigation Funding Agreement",
             "Trial Management Agreement",
             "Witness Deposition Agreement",
             "Judgment Enforcement Agreement",
             "Class Action Settlement Agreement",
             "Conflict Resolution Agreement",
             "Expert Consultation Agreement",
             "Legal Opinion Agreement",
             "Settlement Terms Agreement",
             "Litigation Hold Agreement",
             "Binding Arbitration Agreement",
             "Non-Admission Agreement",
             "Settlement Release Agreement",
             "Litigation Expense Agreement",
             "Attorney-Client Engagement Agreement",
             "Witness Testimony Agreement",
             "Litigation Management Agreement",
             "Legal Consultation Agreement",
             "Legal Support Services Agreement",
             "Settlement Negotiation Agreement",
             "Counterclaim Resolution Agreement",
             "Confidential Settlement Agreement",
             "Expert Testimony Agreement",
             "Litigation Cooperation Agreement",
             "Discovery Plan Agreement",
             "Litigation Strategy Agreement",
             "Pretrial Conference Agreement",
             "Alternative Dispute Resolution Agreement",
             "Negotiated Settlement Agreement",
             "Confidential Information Exchange Agreement",
             "Third-Party Litigation Funding Agreement",
             "Arbitration Award Enforcement Agreement",
             "Class Certification Agreement",
             "Settlement Payment Agreement",
             "Appeal Settlement Agreement",
             "Litigation Cost Sharing Agreement",
             "Litigation Financing Agreement",
             "Settlement Proposal Agreement",
             "Pre-Litigation Resolution Agreement",
             "Mediation Process Agreement",
             "Amendment to Settlement Agreement #5",
             "Amendment to Litigation Services Agreement #3",
             "Amendment to Legal Representation Agreement #2",
             "Amendment to Dispute Resolution Agreement #7",
             "Amendment to Mediation Agreement #1",
             "Amendment to Arbitration Agreement #9",
             "Amendment to Negotiation Services Agreement #6",
             "Amendment to Confidentiality Agreement #8",
             "Non-Disclosure Agreement #12",
             "Release and Waiver Agreement #15",
             "Consent Decree #10",
             "Joint Defense Agreement #13",
             "Expert Witness Agreement #17",
             "Legal Services Retainer Agreement #22",
             "Counseling Services Agreement #14",
             "Pretrial Stipulation Agreement #20",
             "Litigation Funding Agreement #23",
             "Trial Management Agreement #19",
             "Amendment to Witness Deposition Agreement #4",
             "Judgment Enforcement Agreement #28",
             "Class Action Settlement Agreement #31",
             "Conflict Resolution Agreement #27",
             "Expert Consultation Agreement #36",
             "Legal Opinion Agreement #30",
             "Settlement Terms Agreement #35",
             "Amendment to Litigation Hold Agreement #21",
             "Binding Arbitration Agreement #37",
             "Non-Admission Agreement #40",
             "Amendment to Settlement Release Agreement #25",
             "Litigation Expense Agreement #33",
             "Attorney-Client Engagement Agreement #44",
             "Amendment to Witness Testimony Agreement #16",
             "Litigation Management Agreement #42",
             "Legal Consultation Agreement #47",
             "Legal Support Services Agreement #50",
             "Settlement Negotiation Agreement #46",
             "Counterclaim Resolution Agreement #55",
             "Confidential Settlement Agreement #49",
             "Amendment to Expert Testimony Agreement #18",
             "Litigation Cooperation Agreement #52",
             "Amendment to Discovery Plan Agreement #24",
             "Litigation Strategy Agreement #57",
             "Pretrial Conference Agreement #59",
             "Alternative Dispute Resolution Agreement #61",
             "Negotiated Settlement Agreement #63",
             "Confidential Information Exchange Agreement #65",
             "Amendment to Third-Party Litigation Funding Agreement #26",
             "Arbitration Award Enforcement Agreement #67",
             "Class Certification Agreement #69",
             "Settlement Payment Agreement #71",
             "Appeal Settlement Agreement #73",
             "Litigation Cost Sharing Agreement #75",
             "Litigation Financing Agreement #77",
             "Settlement Proposal Agreement #79",
             "Amendment to Pre-Litigation Resolution Agreement #29",
             "Mediation Process Agreement #81",
             "Collaborative Service Agreement",
             "Amalgamated Licensing Contract",
             "Master Services Compact",
             "Reciprocal Non-Disclosure Arrangement",
             "Unified Vendor Agreement",
             "Stipulated Software License",
             "Conclusive Lease Covenant",
             "Harmonious Joint Venture",
             "Congruent Manufacturing Agreement",
             "Symmetrical Distribution Deal",
             "Reciprocal Marketing Partnership",
             "Shared Franchise Agreement",
             "Agreed Purchase Order",
             "Concurring Sales Contract",
             "Joint Employment Pact",
             "Equitable Construction Agreement",
             "Aligned Consulting Engagement",
             "Convergent Supply Agreement",
             "Synchronized Subscription Contract",
             "Reciprocity Service Level Arrangement",
             "Collaborative Loan Agreement",
             "Interlocking Real Estate Lease",
             "Consolidated Settlement Agreement",
             "Unified Investment Contract",
             "Strategic Outsourcing Arrangement",
             "Cooperative Distribution Agreement",
             "Harmonized Licensing Arrangement",
             "Mutual Mergers and Acquisitions Agreement",
             "Congruent Technology Licensing",
             "Symmetrical Employment Contract",
             "Reciprocal Non-Compete Agreement",
             "Shared Confidentiality Pact",
             "Agreed Indemnity Contract",
             "Concurring Retainer Agreement",
             "Joint Supply Chain Deal",
             "Equitable Software Development Contract",
             "Aligned Content Licensing",
             "Convergent Manufacturing Agreement",
             "Synchronized Research Collaboration",
             "Reciprocity Partnership Agreement",
             "Collaborative Strategic Alliance",
             "Interlocking Service Level Agreement",
             "Consolidated Marketing Services Contract",
             "Unified Distribution Partnership",
             "Strategic Software Subscription",
             "Cooperative Sponsorship Agreement",
             "Harmonized Litigation Settlement",
             "Mutual Patent License",
             "Congruent Employment Agreement",
             "Symmetrical Non-Disclosure Contract",
             "Reciprocal Maintenance Services Pact",
             "Shared Joint Venture",
             "Agreed Vendor Agreement",
             "Concurring Master Services Contract",
             "Joint Distribution Agreement",
             "Equitable Lease Contract",
             "SOW",
             "MASTER PRODUCTS AND SERVICES AGREEMENT",
             "Aligned Subscription Services Pact",
             "Convergent Supply Chain Partnership",
             "Synchronized Outsourcing Deal",
             "Reciprocity Marketing Agreement",
             "Collaborative Construction Contract",
             "Interlocking Licensing Arrangement",
             "Consolidated Consulting Engagement",
             "Unified Product Distribution Pact",
             "Strategic Partnership Agreement",
             "Cooperative Service Level Contract",
             "Harmonized Loan Arrangement",
]}  # Set of document types




# def merge_date_lines(text):
#     lines = text.split('\n')
#     i = 0
#     while i < len(lines) - 1:
#         current_line = lines[i].strip()
#         next_line = lines[i + 1].strip()
        
#         if re.search(r'\b(\d{1,2}|\d{4}|January|February|March|April|May|June|July|August|September|October|November|December|DATE)\b', current_line.split()[-1], re.IGNORECASE) and re.search(r'\b(\d{1,2}|\d{4}|January|February|March|April|May|June|July|August|September|October|November|December|DATE)\b', next_line.split()[-1], re.IGNORECASE):
#             lines[i] = current_line + " " + next_line + "\n"
#             del lines[i + 1]
#         else:
#             i += 1

#     return '\n'.join(lines)

# def remove_text_inside_parentheses_and_quotes(text):
#     text = re.sub(r'\([^)]*\)', '', text)  # Remove text inside parentheses
#     text = re.sub(r'"[^"]*"', '', text)    # Remove text inside quotes
#     return text

# def mlingest(new_directory_path, output_path):
#     desired_entities = {"ORG", "DATE", "LAW", "VENDOR", "TYPE"}
#     all_entities = []
    
#     # Use rglob to recursively find all .txt files in the directory and its subdirectories
#     for file_path in new_directory_path.rglob('*.txt'):
#         with open(file_path, 'rt') as file:
#             text = file.read()
        
#         text = remove_text_inside_parentheses_and_quotes(text)
#         doc = nlp(text)
        
#         for ent in doc.ents:
#             if ent.label_ in desired_entities:
#                 all_entities.append(f"{ent.text} ({ent.label_})")

#     with open(output_path, 'wt') as output_file:
#         for line in all_entities:
#             output_file.write(line + '\n')


# === Functions from exportText.py ===
def process_files_in_directory(directory_path, output_directory):
    
    # Get a list of all files in the directory and its subdirectories
    filenames = [os.path.relpath(os.path.join(dirpath, file), directory_path) 
                 for dirpath, dirnames, files in os.walk(directory_path) for file in files]
    
    # Create a pool of worker processes
    pool = Pool(processes=10)  # you can adjust the number of processes

    # Use the pool's map method to apply the process_file function to each filename
    pool.starmap(process_file, [(directory_path, output_directory, filename) for filename in filenames])

    # Close the pool and wait for the worker processes to finish
    pool.close()
    pool.join()


def process_file(directory_path, output_directory, filename):
    try:
        file_path = os.path.join(directory_path, filename)
        if filename.endswith('.pdf'):
            # Use PyPDF2 to get the number of pages
            with open(file_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                num_pages = len(reader.pages)

            # Convert only the first and last pages to images
            pages = convert_from_path(file_path, first_page=1, last_page=num_pages)
            first_page = pages[0]
            last_page = pages[-1 if num_pages > 1 else 0]
            first_page_text = pytesseract.image_to_string(first_page)
            last_page_text = pytesseract.image_to_string(last_page)
            output_filename = os.path.join(output_directory, filename.replace('.pdf', '.txt'))
            text = f"First Page:\n{first_page_text}\n\nLast Page:\n{last_page_text}"

        elif filename.endswith('.docx'):
            doc = Document(file_path)
            paragraphs = [paragraph.text for paragraph in doc.paragraphs]
            pages = '\n'.join(paragraphs).split('\n\n')
            first_page_text = pages[0]
            last_page_text = pages[-1]
            output_filename = os.path.join(output_directory, filename.replace('.docx', '.txt'))
            text = f"First Page:\n{first_page_text}\n\nLast Page:\n{last_page_text}"
        else:
            return
        
        with open(output_filename, 'wt') as output_file:
            output_file.write(text + "\n\n")
            output_file.write("-------------------------------------------------------\n")

    except Exception as e:
        print(f"Error processing {filename}: {e}")

# def format_data_for_training():
#     """
#     This function formats the data for training. It reads from a compiled output file,
#     identifies different entities based on patterns, and re-labels some of them based on
#     predefined criteria. The formatted data is then saved to a new file.
#     """
#     # Load the data from the file
#     with open(Path('files') / 'export' / 'output' / 'postingest' / "compiled_output.txt", "rt") as file:
#         content = file.read()

#     # Function to convert parsed data to spaCy format
#     def convert_to_spacy_format(text, label):
#         # Check if the text is in ORG_SET
#         if text.lower() in ORG_SET:
#             label = "ORG"
#         elif label == "ORG":
#             label = "VENDOR"
#         elif label == "LAW":
#             label = "TYPE"
#         return (text, {"entities": [(0, len(text), label)]})

#     # Parse the content to separate text segments and their corresponding labels
#     pattern = re.compile(r"([^()]+)\s\((ORG|DATE|LAW|CARDINAL|GPE|MONEY|PERSON|TYPE|VENDOR|.+?)\)", re.IGNORECASE)
#     matches = pattern.findall(content)

#     # Convert matches to spaCy training format and adjust the label based on ORG_SET
#     TRAIN_DATA = [convert_to_spacy_format(match[0].strip(), match[1].upper()) for match in matches]

#     # Save the formatted data to a new file
#     with open("updated_formatted_data.txt", "wt") as file:
#         for item in TRAIN_DATA:
#             file.write(str(item) + "\n") 


# Define a function to validate the date label
def validate_date(entity_text, surrounding_text):
    # Attempt to parse the entity text as a date
    try:
        # Check if "effective" is present in the surrounding text
        if surrounding_text:  # Check if surrounding_text is not None
            if "effective" in surrounding_text.lower():
                return entity_text  # Return the entity text as it follows "effective"

        # Attempt to parse the entity text as a date
        parsed_date = parser.parse(entity_text, fuzzy=True)

        # Check if the parsed date contains a year, month, and day
        if parsed_date.year and parsed_date.month and parsed_date.day:
            return parsed_date.strftime('%m-%d-%Y')  # Return a standardized date format (YYYY-MM-DD)
    except ValueError:
        pass  # Parsing failed, treat it as an incomplete date or invalid date format

    return None  # Invalid or incomplete date

def validate_type(entity_text):
    # Check if the entity text contains the word "this"
    if "this" in entity_text.lower():
        return entity_text  # Return the entity text if it contains "this"
    
    # If "this" is not present, return None to indicate that we haven't found a valid type yet
    return None


# Define a function to validate the vendor label
def validate_vendor(entity_text):
    # Check if the entity text contains "DISH" in any form and return None if it does
    if "dish" in entity_text.lower():
        return None
    return entity_text  # Return the original entity text

# Main script



def process_entity(entity, lines, entities_found):
    """
    Process a given entity, validate it, and add it to the entities_found dictionary if valid.

    Parameters:
    - entity: The entity to process
    - lines: The lines of the original text to check surrounding context
    - entities_found: The dictionary of already found entities

    Returns:
    - entities_found: Updated dictionary of found entities
    - all_found: Boolean indicating if all desired entities are found
    """
    matched_entities = set()

    # Desired entities to check
    desired_entities = {"VENDOR", "DATE", "TYPE"}
    # Check if the entity's text has already been matched
    if entity.text not in matched_entities:
        matched_entities.add(entity.text)

    # Find the line containing the entity
    entity_line = next((line for line in lines if entity.text in line), None)

    # Skip processing if the entity's text is in the ORG_SET
    if entity.text.lower() in ORG_SET:
        return entities_found, False

    # Process entity based on its label or text
    if entity.text.lower() in TYPE_SET and "TYPE" not in entities_found:
        type_value = validate_type(entity.text)
        if type_value:
            entities_found["TYPE"] = type_value
    elif entity.label_ == "ORG" and "VENDOR" not in entities_found:
        vendor_value = validate_vendor(entity.text)
        if vendor_value:
            entities_found["VENDOR"] = vendor_value
    elif entity.label_ == "DATE" and "DATE" not in entities_found:
        date_value = validate_date(entity.text, entity_line)
        if date_value:
            entities_found["DATE"] = date_value
    elif entity.label_ == "LAW" and "TYPE" not in entities_found:
        type_value = validate_type(entity.text)
        if type_value:
            entities_found["TYPE"] = type_value

    # Check if we've found all desired entities
    all_found = all(key in entities_found for key in desired_entities)

    return entities_found, all_found
def extract_entities_from_files():
    # nlp = spacy.load(Path('files') / 'models')
    base_directory_path = Path('files') / 'export' / 'output'
    result_files_directory = Path('files') / 'export' / 'output' / 'entities'

    # Ensure the result directory exists
    result_files_directory.mkdir(parents=True, exist_ok=True)

    # Iterate through the directories and subdirectories using os.walk
    for directory_path, _, filenames in os.walk(base_directory_path):
        for filename in filenames:
            if filename.startswith('results_'):  # Check if the file has already been processed
                continue  # Skip processing this file
                
            if filename.endswith('.txt'):  # Check if the file is a text file
                
                # Name of the output file based on the input file name
                output_filename = f"results_{filename}"
                output_path = os.path.join(result_files_directory, output_filename)
                
                # Check if the results file already exists
                if Path(output_path).exists():
                    continue  # Skip processing this file
                
                file_path = os.path.join(directory_path, filename)

                # The "with open" statement should be within the ".txt" check.
                with open(file_path, "rt") as in_file, open(output_path, "wt") as out_file:
                    text = in_file.read()
                    doc = nlp(text)
                    entities_found = {}
                    lines = text.split('\n')

                    for ent in doc.ents:
                        entities_found, _ = process_entity(ent, lines, entities_found)  # Unpack the tuple

                    for label, entity in entities_found.items():
                        out_file.write(f"{entity} - {label}\n")


                    
                    
                    
                    
                    
                    
main_file_path = Path('files') / 'export'
text_files_path = Path('files') / 'export' / 'output' / 'entities'

def read_entity_values_from_file(file_path):
    with open(file_path, 'rt') as file:
        entity_values = {"VENDOR": [], "TYPE": [], "DATE": []}
        for line in file.readlines(): 
            if '-' not in line:
                continue
            entity_value, entity_type = line.rsplit('-', 1)
            entity_type = entity_type.strip()
            entity_value = entity_value.strip()
            if entity_type == 'TYPE':
                entity_value = re.sub(r'^\b(of|in|on|for|the|this)\b\s*', '', entity_value, flags=re.IGNORECASE) 
            if entity_type in entity_values:
                entity_values[entity_type].append(entity_value)
        
        first_entity_values = {k: select_most_appropriate_value(v) for k, v in entity_values.items()}
    
    return first_entity_values

def select_most_appropriate_value(values):
    for value in values:
        if value:
            for date_format in ['%B %d, %Y', '%B, %Y', '%B %Y']:
                try:
                    datetime.strptime(value, date_format)
                    return value
                except ValueError:
                    continue
            return value
    return None

def rename_pdf(pdf_file_path, entity_values, parent_folder_name):
    pdf_file_stem = pdf_file_path.stem
    if entity_values.get('DATE'):
        valid_date_found = False
        try:
            for date_format in ['%B %d, %Y', '%B, %Y', '%B %Y']:
                try:
                    formatted_date = datetime.strptime(entity_values['DATE'], date_format).strftime('%m-%d-%y')
                    entity_values['DATE'] = formatted_date
                    valid_date_found = True
                    break
                except ValueError:
                    continue
        except ValueError:
            pass
        
        if not valid_date_found:
            entity_values['DATE'] = None
                
    new_file_name_entities = [
        entity_values.get('VENDOR'),
        entity_values.get('TYPE'),
        parent_folder_name,
        entity_values.get('DATE')
    ]
    
    new_file_name = '_'.join(filter(None, new_file_name_entities))
    abs_path = os.path.abspath(pdf_file_path)
    directory, filename = os.path.split(abs_path)
    base, extension = os.path.splitext(filename)
    os.rename(abs_path, os.path.join(directory, new_file_name + extension)) 

def rename_files():
    for folder in main_file_path.iterdir():
        if folder.is_dir():
            for pdf_file_path in folder.rglob('*.pdf'):
                pdf_file_stem = pdf_file_path.stem
                txt_file_name = f"results_{pdf_file_stem}.txt"
                txt_file_path = text_files_path / txt_file_name
                if txt_file_path.exists():
                    try:
                        entity_values = read_entity_values_from_file(txt_file_path)
                        parent_folder_name = folder.name
                        rename_pdf(pdf_file_path, entity_values, parent_folder_name)
                    except Exception as e:
                        print(f"Error renaming {pdf_file_path.name}: {e}")

def delete_files_in_subdirectories(directory_path):
    """Delete all files within the subdirectories of the specified directory, but not the subdirectories themselves.
    
    Args:
        directory_path (Path): The path to the directory.
        
    Returns:
        None
    """
    for subdir in os.listdir(directory_path):
        subdir_path = os.path.join(directory_path, subdir)
        if os.path.isdir(subdir_path):
            for filename in os.listdir(subdir_path):
                file_path = os.path.join(subdir_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.remove(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")


# === Main function ===
def main():
    """Main function to coordinate the execution of the entire workflow.
    Returns:
        None
    """
    # Define the input and output directory paths (update with actual paths later)
    directory_path = Path('files') / 'export' 
    # new_directory_path = Path('files') / 'export' / 'output'
    # new_output_path = Path('files') / 'export' / 'output' / 'postingest'
    # output_filename = "compiled_output.txt"
    # output_path = os.path.join(new_output_path, output_filename)
    # new_output_path.mkdir(parents=True, exist_ok=True)
    
    process_files_in_directory(directory_path, output_directory)
    
    if not output_directory.exists():
        output_directory.mkdir(parents=True)

    # Define the set of spaCy entity labels to focus on during the NER process
    entity_labels = {"ORG", "DATE", "LAW", "VENDOR", "TYPE"}  # Update with the actual entity labels you want to focus on

    # Step 1: Process files in the input directory to extract texts from the first and last pages
    with ProcessPoolExecutor() as executor:
        list(executor.map(process_file, [input_directory] * len(os.listdir(input_directory)), [output_directory] * len(os.listdir(input_directory)), os.listdir(input_directory)))
    

    # Step 2: Process the extracted text files using spaCy for named entity recognition (NER)


    # mlingest(new_directory_path, output_path)

    # Step 3: Integrate and call functions from MLFormat.py
    # format_data_for_training()
    
    # Step 4: Integrate and call functions from MLModelTest.py
    extract_entities_from_files()
    # Step 5: Integrate and call functions from renameFileTest.py
    rename_files()
    
    delete_files_in_subdirectories(output_directory)


    print("Workflow completed.")


if __name__ == "__main__":
    main()


            
