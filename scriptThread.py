
# Adjust the PATH environment variable to include poppler binaries
import os
# os.environ["PATH"] += os.pathsep + "/usr/local/Cellar/poppler/23.08.0/bin"
os.environ["PATH"] += os.pathsep + "/opt/homebrew/Cellar/poppler/poppler/bin"


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


import sys
from concurrent.futures import ThreadPoolExecutor
import shutil 
from PyQt6.QtCore import QThread, pyqtSignal
from datetime import datetime
from docx import Document 
from pathlib import Path
import logging
import os
import platform
import ctypes
import pdf2image

# Set up logging

import logging

# Set up logging
log_filename = os.path.expanduser('~/Desktop/app_log.txt')
logging.basicConfig(filename=log_filename, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Script started.")

logging.basicConfig(filename=log_filename, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Script started.")

import PyPDF2
from pdf2image import convert_from_path
from dateutil import parser
from os import walk
import os
os.environ['QT_OPENGL'] = 'software'
import pytesseract

if getattr(sys, 'frozen', False):  # running as a bundled executable
    pytesseract.pytesseract.tesseract_cmd = resource_path('/opt/homebrew/Cellar/tesseract/5.3.3/bin/tesseract')
else:  # running in a development environment
    pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/Cellar/tesseract/5.3.3/bin/tesseract'



import re
import gc
import spacy

# documents_folder = Path(self.base))

# input_directory = documents_folder / 'Renamed Files' / 'export'
# output_directory = documents_folder / 'Renamed Files' / 'export' / 'output'

if getattr(sys, 'frozen', False):
    # Running as a bundled executable with PyInstaller
    base_path = sys._MEIPASS
else:
    # Running in a normal Python environment
    base_path = '/opt/homebrew/lib/python3.11/site-packages'

# Load the English language model for spaCy
# model_path = os.path.join(base_path, "en_core_web_md")  # Use base_path here
model_path = ("/opt/homebrew/lib/python3.11/site-packages/en_core_web_md")  # Use base_path here
nlp = spacy.load(model_path, disable=["transformer"])

# nlp.disable_pipe("parser")
# nlp.enable_pipe("senter")


# def get_resource_path(relative_path):
#     """ Get the absolute path to the resource, works for dev and for PyInstaller """
#     base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
#     return os.path.join(base_path, relative_path)

# model_path = get_resource_path('files/models')
# nlp = spacy.load(model_path)


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
           "Sling TV L.L.C."
           "Blockbuster LLC",
           "Sling Media Inc.",
           "AirTV L.L.C.",
           "Dish Network Canada ULC",
           "Dish Mexico, S. de R.L. de C.V.",
           ]}  # Set of organization names
TYPE_SET = {type.lower() for type in ["Statement of Work",
             "Master Services Agreement",
             "Non-Disclosure Agreement",
             "Set Top Box Agreement",
             "Attachment No. 1",
             "Technical Support Services Renewal Order",
             "gTLD Services Agreement",
             "Non Disclosure Agreement",
             "Application Master Agreement",
             "Mutual Non-Disclosure Agreement",
             "Memorandum -- Contract-to-Hire",
             "Memorandum - Contract-to-Hire",
             "Amendment to Master Purchasing Agreement",
             "Agreement for Professional Services",
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
             "Amendment #2 to Statement of Work",
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
             "MASTER SUBSCRIPTION AGREEMENT",
             "Memorandum - Contractor",
             "Memorandum - Contractor(s)",
             "Operating Lease Agreement",
             "Maintenance Agreement",
             "Collaboration Agreement",
             "Research and Development Agreement",
             "Indemnification Agreement",
             "Power of Attorney",
             "Royalty Agreement",
             "Memorandum",
             "Memorandum of Understanding",
             "Comarketing & Service Agreement",
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
             "Partner Agreement",
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
             "Call Center Services Agreement,"
             "Master Service Agreement",
             "Program Distribution Agreement",
             "Distribution Rights Agreement",
             "Broadcast Syndication Agreement",
             "Video Streaming Agreement",
             "Satellite Transmission Services Agreement",
             "Technical Equipment Agreement",
             "Co-Branding Agreement",
             "Co-Marketing & Service Agreement",
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
             "Amendment One to the Non-Disclosure Agreement",
             "Mutual Nondisclosure Agreement",
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
             "Amendment #7",
             "Amendment #6",
             "Amendment #5",
             "Amendment #4",
             "Amendment #3",
             "Amendment #2",
             "Amendment #1",
             "Amendment #8",
             "Amendment #9",
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
             "STATEMENT OF WORK No. 1",
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
processed_files = set()

class ScriptThread(QThread): 
    
    error_signal = pyqtSignal(list)  # Signal to emit errors
    progress_signal = pyqtSignal(int)  # Signal to emit progress percentage
    status_signal = pyqtSignal(str)  # Signal to emit status updates
    
    def __init__(self, base_directory, parent=None, total_files=0):  # Accept total_files as an argument
        super().__init__()
        super(ScriptThread, self).__init__(parent)
        self.base_directory = base_directory 
        self.total_files = total_files  # Store total_files
        # Create the 'Unknown' folder
        self.unknown_folder = Path(self.base_directory) / 'Renamed Files' / 'export' / 'INCOMPLETE'
        self.unknown_folder.mkdir(parents=True, exist_ok=True)

    
    def run(self):
        documents_folder = Path(self.base_directory)
        output_directory = documents_folder / 'Renamed Files' / 'export' / 'output'
        directory_path = documents_folder / 'Renamed Files' / 'export'
        old_directory_path = documents_folder / 'Renamed Files' / 'export' / 'output'
        
        errors = []
        # Count files in the directory and its subdirectories
        file_count = sum(len(files) for _, _, files in os.walk(directory_path)) 
        
        def update_progress(progress):
            # Multiply the progress by 0.4 since this step is allocated 40% of the total progress
            self.progress_signal.emit(int(progress * 0.4))
        
        try:
            # Step 1: Process files (50% of total progress)
            self.status_signal.emit(f"Processing files...")
            process_files_in_directory(directory_path, output_directory, callback=update_progress)
            self.progress_signal.emit(40) 
            
            # Step 2: Extract entities (up to 80% of total progress)
            self.status_signal.emit("Extracting entities...")
            extract_entities_from_files(self)
            self.progress_signal.emit(70)

            # Step 3: Rename files (100% of total progress)
            self.status_signal.emit("Renaming files...")
            rename_files(self)
            self.progress_signal.emit(80)
            
            # Step 4: Cleanup
            self.status_signal.emit("Cleaning up...")
            # hide_directory(old_directory_path)
            self.progress_signal.emit(100)

            self.status_signal.emit("Files ReNAMEd successfully!")
        
        except Exception as e:
            logging.exception('Error encountered:')
            errors.append(f"Error: {str(e)}")
            self.error_signal.emit(errors)    


def process_file(directory_path, output_directory, filename):
    print(f"Processing: {filename} from {directory_path} to {output_directory}")

    # Set the path for pdf2image to find poppler utilities
    poppler_path = resource_path("poppler/bin")
    pdf2image.poppler_path = poppler_path
    


    
    try:
        file_path = os.path.join(directory_path, filename)
        if filename.endswith('.pdf'):
            with open(file_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                num_pages = len(reader.pages)

           
            # So, we'll create a list of pages we want to process.
            pages_to_process = [1, num_pages]

            texts = []
            for page_num in pages_to_process:
                # Convert one page at a time
                page_image = convert_from_path(file_path, first_page=page_num, last_page=page_num)[0]
                logging.info('Extracting text using pytesseract.')
                page_text = pytesseract.image_to_string(page_image).strip()
                texts.append(page_text)

                # Free up the memory used by the image
                del page_image
                gc.collect()

            # Remove lines containing "processing" from the first page text
            first_page_text = texts[0]
            first_page_lines = first_page_text.split('\n')
            first_page_lines = [line for line in first_page_lines if 'processing' not in line.lower()]
            first_page_text = '\n'.join(first_page_lines)

            last_page_text = texts[1] if len(texts) > 1 else first_page_text

            output_filename = os.path.join(output_directory, filename.replace('.pdf', '.txt'))
            text = f"{first_page_text}\n\n{last_page_text}"

        elif filename.endswith('.docx'):
            doc = Document(file_path)
            paragraphs = [paragraph.text.strip() for paragraph in doc.paragraphs]
            pages = '\n'.join(paragraphs).split('\n\n')
            first_page_text = pages[0].strip()
            last_page_text = pages[-1].strip()
            output_filename = os.path.join(output_directory, filename.replace('.docx', '.txt'))
            
            # Remove lines containing "processing" from the first page text
            first_page_lines = first_page_text.split('\n')
            first_page_lines = [line for line in first_page_lines if 'processing' not in line.lower()]
            first_page_text = '\n'.join(first_page_lines)
            
            text = f"{first_page_text}/n/n{last_page_text}"
        else:
            return
        
        with open(output_filename, 'wt') as output_file:
            output_file.write(text + "\n\n")
            output_file.write("-------------------------------------------------------\n")

    except Exception as e:
        logging.exception('Error encountered:')
        print(f"Error processing {filename}: {e}")
        # Move the problematic file to the designated error folder
        # Move the problematic file directly to the "Not Renamed" directory
        dest_path = Path(directory_path) / 'INCOMPLETE'
        shutil.move(file_path, dest_path)



    

def process_files_in_directory(directory_path, output_directory, callback=None):
    filenames = [os.path.relpath(os.path.join(dirpath, file), directory_path) 
                 for dirpath, _, files in os.walk(directory_path) for file in files]
    
    total_files = len(filenames)
    total_processed = 0

    with ThreadPoolExecutor() as executor:
        futures = []
        for i in range(total_files):
            file_to_process = filenames[i]
            
            # Check if the file has already been processed (renamed)
            if os.path.basename(file_to_process) not in processed_files:
                futures.append(executor.submit(process_file, directory_path, output_directory, file_to_process))

        for future in futures:
            _ = future.result()  # This will raise any exceptions that occurred during function execution
            total_processed += 1
            if callback:
                progress = total_processed * 100 / total_files
                callback(progress)



def threaded_process_files(self, directory_path, output_directory, callback):
    with ThreadPoolExecutor() as executor:
        # Generate all file paths you want to process
        filenames = [os.path.relpath(os.path.join(dirpath, file), directory_path) 
                     for dirpath, _, files in os.walk(directory_path) for file in files]
        
        futures = [executor.submit(self.process_file, directory_path, output_directory, filename) for filename in filenames]

        
        for future in futures:
            future.result()  # This will raise any exceptions that occurred during function execution
            if callback:
                callback()  # Call the callback if provided


def get_surrounding_text(lines, entity_text, max_lines=4):
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

# Define a function to get the line before the entity line as previous text
def get_previous_line(lines, entity_text, max_lines=4):
    previous_lines = []

    for line in lines:
        if entity_text in line:
            break  # Stop when the entity line is found

        previous_lines.append(line)

        if len(previous_lines) >= max_lines:
            break  # Stop collecting lines if max_lines is reached

    return " ".join(previous_lines).strip()



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

def validate_type(entity_text, surrounding_text):
    valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#.- "  # Define a list of valid characters

    # Filter out invalid characters from the entity_text
    valid_entity_text = ''.join(char for char in entity_text if char in valid_chars)

    # If the entity_text is a direct match in TYPE_SET, return it
    if entity_text.lower() in TYPE_SET:
        return entity_text

    # If the valid_entity_text is a direct match in TYPE_SET, return it
    if valid_entity_text.lower() in TYPE_SET:
        return valid_entity_text

    # If none of the above, check if any of the TYPE_SET values are in the surrounding_text
    for type_label in TYPE_SET:
        if type_label in surrounding_text.lower():  # Check for a match in TYPE_SET within the surrounding text
            return type_label.title()  # Return the exact match from TYPE_SET

    return None




def validate_vendor(entity_text):
    valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789&- "  # Define a list of valid characters

    # List of common personal names or keywords specific to individuals
    personal_names = ["atilla", "tinic"]  # Add more as needed
    
    # Exclusion list for potential vendor names
    VENDOR_EXCLUSIONS = {"agreement", "contract", "amendment", "lease", "effective", "disclosing", "amendmnt", "statement of work", "master services agreement", "the master products", "statement", "received", "windows server", "mimecast education", "customer data", "confidential information", "description of services and compensation", "foreign language content", "hiringdelivery", "professional services", "purpose", "resource service order", "retail wireless technology", "rightfax", "security solutions architect", "service order", "syncronization", "the servicesandor software", "thecompany", "therefore", "mvno & retail wireless"}  # Add more as needed

    # Filter out invalid characters from the entity_text
    valid_entity_text = ''.join(char for char in entity_text if char in valid_chars).lower()  # Convert to lowercase

    if (
        "dish" not in valid_entity_text and
        "DNLLC" not in valid_entity_text and
        "dpc" not in valid_entity_text and
        "sling" not in valid_entity_text and
        "echostar" not in valid_entity_text and
        valid_entity_text not in TYPE_SET and  # Ensure valid_entity_text is not in TYPE_SET
        entity_text not in ORG_SET and
        all(name not in valid_entity_text for name in personal_names) and
        not contains_consecutive_numbers(valid_entity_text) and  # Check for consecutive numbers
        not any(exclusion in valid_entity_text for exclusion in VENDOR_EXCLUSIONS)  # Check for vendor exclusions
    ):
        if valid_entity_text:
            return valid_entity_text.title()  # Return the filtered entity_text

    return None




def contains_consecutive_numbers(text):
    # Function to check if text contains three or more consecutive numbers
    consecutive_numbers = 0
    for char in text:
        if char.isdigit():
            consecutive_numbers += 1
            if consecutive_numbers >= 3:
                return True
        else:
            consecutive_numbers = 0
    return False
# Main script 

def process_entity(entity, lines, entities_found):

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
def extract_entities_from_files(self):
    # nlp = spacy.load(Path('Renamed Files') / 'models')
    documents_folder = Path(self.base_directory)

    directory_path = documents_folder / 'Renamed Files' / 'export' / 'output'
    result_files_directory = documents_folder / 'Renamed Files' / 'export' / 'output' / 'entities'

    # Ensure the result directory exists
    result_files_directory.mkdir(parents=True, exist_ok=True)
    if not result_files_directory.exists():
        raise ValueError(f"Failed to create directory: {result_files_directory}")

    # Initialize sets and lists to store matched entities and available entities
    matched_entities = set()
    desired_entities = {"VENDOR", "DATE", "TYPE"}
    available_dates = []
    available_vendors = []
    available_types = []

    # Initialize a set to store processed file names
    # processed_files = set()

    # Iterate through the input files
    for current_directory, _, filenames in os.walk(directory_path):
        for filename in filenames:
            if filename.endswith('.txt'):
                file_path = os.path.join(current_directory, filename)
                rel_file_path = os.path.relpath(file_path, start=directory_path)

                # Ensure that the file is within the specified directory and not processed
                original_filename = filename.replace('results_', '')
                if rel_file_path.startswith('..') or original_filename in processed_files:
                    continue

                output_filename = f"results_{filename}"
                output_path = os.path.join(result_files_directory, output_filename)

                if not os.path.exists(output_path):
                    processed_files.add(original_filename)

                    with open(file_path, "rt") as in_file, open(output_path, "wt") as out_file:
                        text = in_file.read()
                        doc = nlp(text)
                        lines = text.split('\n')
                        entities_found = {}
                        found_date, found_vendor, found_type = False, False, False

                        # Prioritize checking for TYPE
                        for ent in doc.ents:
                            if ent.text.lower() in TYPE_SET or ent.label_ == "LAW":
                                type_value = validate_type(ent.text, get_surrounding_text(lines, ent.text))
                                if type_value:
                                    entities_found["TYPE"] = type_value
                                    found_type = True
                                    available_types.append(type_value)

                        # Process other entities
                        for ent in doc.ents:
                            if ent.text in matched_entities or ent.text in TYPE_SET:
                                continue

                            matched_entities.add(ent.text)
                            surrounding_text = get_surrounding_text(lines, ent.text)

                            if ent.text in ORG_SET:
                                continue
                            elif ent.label_ == "ORG":
                                label = "VENDOR"
                                vendor_value = validate_vendor(ent.text)
                                if vendor_value and not found_vendor:
                                    entities_found["VENDOR"] = vendor_value
                                    found_vendor = True
                                    available_vendors.append(vendor_value)
                            elif ent.label_ == "DATE":
                                label = "DATE"
                                date_value = validate_date(ent.text, surrounding_text)
                                if date_value and not found_date:
                                    entities_found["DATE"] = date_value
                                    found_date = True
                                    available_dates.append(date_value)

                            if found_date and found_vendor and found_type:
                                break

                        # Populate missing entities from available lists
                        for label in desired_entities:
                            if label not in entities_found:
                                if label == "DATE" and available_dates:
                                    entities_found[label] = available_dates.pop(0)
                                elif label == "TYPE" and available_types:
                                    entities_found[label] = available_types.pop(0)
                                elif label == "VENDOR" and available_vendors:
                                    entities_found[label] = available_vendors.pop(0)
                                else:
                                    entities_found[label] = ""

                        # Write the entities to the output file
                        for label, entity in entities_found.items():
                            if entity:
                                out_file.write(f"{entity} - {label}\n")

                                        
def read_entity_values_from_file(file_path):
    with open(file_path, 'rt') as file:
        lines = file.readlines()

        # Check the first two lines for TYPE entity
        primary_type_value = None
        for line in lines[:4]:
            if '- TYPE' in line:
                primary_type_value = line.split('- TYPE')[0].strip()
                break

        entity_values = {"VENDOR": [], "TYPE": [], "DATE": []}
        for line in lines: 
            if '-' not in line:
                continue
            entity_value, entity_type = line.rsplit('-', 1)
            entity_type = entity_type.strip()
            entity_value = entity_value.strip()

            if entity_type == 'TYPE':
                if primary_type_value:
                    # If we've already identified a primary type value from the first two lines, use that
                    entity_values[entity_type].append(primary_type_value)
                    primary_type_value = None  # Clear it after using it once
                else:
                    entity_values[entity_type].append(entity_value)
            else:
                entity_values[entity_type].append(entity_value)
        
        first_entity_values = {k: select_most_appropriate_value(v) for k, v in entity_values.items()}
    print(first_entity_values)
    return first_entity_values



def select_most_appropriate_value(values):
    # Just return the first non-empty value from the list or None if no such value exists
    return next((value for value in values if value), None)


def rename_pdf(pdf_file_path, entity_values, parent_folder_name):
    
    if entity_values.get('DATE'):
        valid_date_found = False
        try:
            formatted_date = datetime.strptime(entity_values['DATE'], '%m-%d-%Y').strftime('%m-%d-%y')
            entity_values['DATE'] = formatted_date
            valid_date_found = True
        except ValueError:
            pass
        
        if not valid_date_found:
            entity_values['DATE'] = None
            
                
    # Ensure TYPE is always present
    entity_values['TYPE'] = entity_values.get('TYPE') or "UnknownType"
    entity_values['VENDOR'] = entity_values.get('VENDOR') or "UnknownVendor"

    

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
    new_file_path = os.path.join(directory, new_file_name + extension)
    
    os.rename(abs_path, new_file_path)
    
    # Add the renamed file name to the set
    processed_files.add(os.path.basename(new_file_path))


def rename_files(self):
    main_file_path = Path(self.base_directory) / 'Renamed Files' / 'export'
    text_files_path = main_file_path / 'output' / 'entities' 
    
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
                        
                        # After renaming, update the pdf_file_path to point to the new filename
                        new_file_name = f"{entity_values.get('VENDOR', '')}_{entity_values.get('TYPE', '')}_{parent_folder_name}_{entity_values.get('DATE', '')}.pdf"
                        updated_pdf_file_path = pdf_file_path.parent / new_file_name
                        
                        # Check if the word 'UnknownType' or 'UnknownVendor' is in the new file name
                        if "UnknownType" in updated_pdf_file_path.stem or "UnknownVendor" in updated_pdf_file_path.stem:
                            shutil.move(updated_pdf_file_path, self.unknown_folder / updated_pdf_file_path.name)
                            
                            
                    except Exception as e:
                        logging.exception('Error encountered:')
                        print(f"Error renaming {pdf_file_path.name}: {e}")


# def delete_directory(old_directory_path):
 
#     try:
#         shutil.rmtree(old_directory_path)
#         print(f"Deleted directory: {old_directory_path}")
#     except Exception as e:
#         logging.exception('Error encountered:')
#         print(f"Failed to delete {old_directory_path}. Reason: {e}")


# === Main function ===
def main(self):

    # Set the base directory to the user's Documents/Renamed Files folder
    base_dir = Path(self.base_directory)

    # Using the base directory in the paths
    directory_path = base_dir / 'export'
    old_directory_path = directory_path / 'output'
    output_directory = directory_path / 'output'

    
    process_files_in_directory(directory_path, output_directory)
    
    # if not output_directory.exists():
    #     output_directory.mkdir(parents=True)

    # Define the set of spaCy entity labels to focus on during the NER process
    entity_labels = {"ORG", "DATE", "LAW", "VENDOR", "TYPE"}  # Update with the actual entity labels you want to focus on

    extract_entities_from_files()
    
    # Step 5: Integrate and call functions from renameFileTest.py
    rename_files()
    
    # delete_directory(old_directory_path)

    
if __name__ == "__main__":
        main()
