import spacy
import os
from pathlib import Path
from dateutil import parser
import re

# Load your trained model
nlp = spacy.load(Path('files') / 'models')

directory_path = Path('files') / 'export' / 'output'
result_files_directory = Path('files') / 'export' / 'output' / 'entities'

# Ensure the result directory exists
result_files_directory.mkdir(parents=True, exist_ok=True)

# Initialize sets to store matched entities
matched_entities = set()

# Desired entities to check
desired_entities = {"VENDOR", "DATE", "TYPE"}

# Initialize lists to store available entities for each label
available_dates = []
available_vendors = []
available_types = []

# List of Dish Entity names
ORG_SET = {org.lower() for org in ["American H Block Wireless, L.L.C.", 
           "Blockbuster, L.L.C.", 
           "CMBSat", "DBSD Corporation", 
           "DCS",
           "DPC",
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


# List of Agreement Type names

TYPE_SET = {type.lower() for type in [ "Statement of Work",
             "Master Services Agreement",
             "Non-Disclosure Agreement",
             "Amendment to Master Purchasing Agreement",
             "Lease Agreement",
             "Employment Contract",
             "Licensing Agreement",
             "Utility Services Statement of Work"
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
]}

# Define a function to get the line before the entity line as surrounding text
def get_surrounding_text(lines, entity_text, max_lines=1):
    surrounding_text = ""
    entity_found = False
    lines_before_entity = []
    lines_after_entity = []

    for line in lines:
        if entity_text in line:
            entity_found = True
            continue

        if entity_found:
            if len(lines_after_entity) < max_lines:
                lines_after_entity.append(line)
        else:
            if len(lines_before_entity) < max_lines:
                lines_before_entity.append(line)

    surrounding_text += " ".join(lines_before_entity[::-1]) + " "  # Reverse lines_before_entity
    surrounding_text += " ".join(lines_after_entity)

    return surrounding_text.strip()

def validate_date(entity_text, surrounding_text):
    # Define a regular expression pattern to match alphanumeric date components
    alphanumeric_pattern = re.compile(r'[a-zA-Z0-9]+')

    # Extract alphanumeric date components from the entity text
    alphanumeric_date = ' '.join(alphanumeric_pattern.findall(entity_text))

    if alphanumeric_date:
        try:
            # Attempt to parse the extracted alphanumeric date
            parsed_date = parser.parse(alphanumeric_date, fuzzy=True)
            if parsed_date.year and parsed_date.month and parsed_date.day:
                return parsed_date.strftime('%m-%d-%Y')  # Return a standardized date format (YYYY-MM-DD)
        except ValueError:
            pass  # Parsing failed, treat it as an incomplete date or invalid date format

    if "effective" in surrounding_text.lower():
        return entity_text  # Return the entity text as it follows "effective"

    return None  # Invalid or incomplete date

def validate_vendor(entity_text):
    valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789&- "  # Define a list of valid characters

    if "dish" not in entity_text.lower() and "dpc" not in entity_text.lower() and entity_text not in ORG_SET:
        # Filter out invalid characters from the entity_text
        valid_entity_text = ''.join(char for char in entity_text if char in valid_chars)

        if valid_entity_text:
            return valid_entity_text  # Return the filtered entity_text

    return None

def validate_type(entity_text, surrounding_text):
    valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#.- "  # Define a list of valid characters

    if "this" in entity_text.lower() or "(" in surrounding_text.lower() or "section" not in entity_text.lower():
        # Filter out invalid characters from the entity_text
        valid_entity_text = ''.join(char for char in entity_text if char in valid_chars)

        if valid_entity_text:
            return valid_entity_text  # Return the filtered entity_text

    for type_label in TYPE_SET:
        if type_label in surrounding_text.lower():
            # Filter out invalid characters from the found type_label
            valid_type_label = ''.join(char for char in type_label if char in valid_chars)

            if valid_type_label:
                return valid_type_label  # Return the filtered type_label

    return None

# Main script

# Iterate through the input files
# Initialize a set to store processed file names
processed_files = set()

# Iterate through the input files
for current_directory, _, filenames in os.walk(directory_path):
    for filename in filenames:
        if filename.endswith('.txt'):
            file_path = os.path.join(current_directory, filename)
            
            # Calculate the relative path of the file
            rel_file_path = os.path.relpath(file_path, start=directory_path)
            
            # Ensure that the file is within the specified directory
            if not rel_file_path.startswith('..'):
                # Check if the original file (without "results_") has already been processed
                original_filename = filename.replace('results_', '')
                if original_filename in processed_files:
                    continue

                # Name of the output file based on the input file name
                output_filename = f"results_{filename}"
                output_path = os.path.join(result_files_directory, output_filename)

                # Check if the output file already exists, and if it does, skip processing
                if not os.path.exists(output_path):
                    # Add the original file (without "results_") to the set of processed files
                    processed_files.add(original_filename)

                    with open(file_path, "rt") as in_file, open(output_path, "wt") as out_file:
                        text = in_file.read()
                        doc = nlp(text)
                        entities_found = {}
                        lines = text.split('\n')

                        found_date = False
                        found_vendor = False
                        found_type = False

                        for ent in doc.ents:
                            if ent.text not in matched_entities:
                                matched_entities.add(ent.text)

                                surrounding_text = get_surrounding_text(lines, ent.text)
                                entity_line = next((line for line in lines if ent.text in line), None)

                                if ent.text in ORG_SET:
                                    continue
                                elif ent.text in TYPE_SET or ent.label_ == "LAW":
                                    label = "TYPE"
                                elif ent.label_ == "ORG":
                                    label = "VENDOR"
                                else:
                                    label = ent.label_

                                if label == "DATE" and not found_date:
                                    date_value = validate_date(ent.text, surrounding_text)
                                    if date_value:
                                        entities_found["DATE"] = date_value
                                        found_date = True
                                        available_dates.append(date_value)

                                if label == "VENDOR" and not found_vendor:
                                    vendor_value = validate_vendor(ent.text)
                                    if vendor_value:
                                        entities_found["VENDOR"] = vendor_value
                                        found_vendor = True
                                        available_vendors.append(vendor_value)

                                if label == "TYPE" and not found_type:
                                    type_value = validate_type(ent.text, surrounding_text)
                                    if type_value:
                                        entities_found["TYPE"] = type_value
                                        found_type = True
                                        available_types.append(type_value)

                                if found_date and found_vendor and found_type:
                                    break

                        for label in desired_entities:
                            if label not in entities_found:
                                if label == "DATE" and available_dates:
                                    entities_found[label] = available_dates.pop(0)
                                elif label == "VENDOR" and available_vendors:
                                    entities_found[label] = available_vendors.pop(0)
                                elif label == "TYPE" and available_types:
                                    entities_found[label] = available_types.pop(0)

                        for label in desired_entities:
                            if label not in entities_found:
                                entities_found[label] = ""

                        for label, entity in entities_found.items():
                            if entity:
                                out_file.write(f"{entity} - {label}\n")

