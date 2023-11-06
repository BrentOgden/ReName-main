import PyPDF2
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer 
import string

def preprocess_and_tokenize(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    return tokens


def extract_text_from_pdf_with_ocr(file_path):
    # Convert the PDF page(s) to images
    images = convert_from_path(file_path)
    
    # Since we're only interested in the first page:
    first_page_image = images[0]

    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(first_page_image)

    return text

text = extract_text_from_pdf_with_ocr('files/Volks Resources LLC (Workspend) - Triparty Supplier Agreement (FE) (6.22.23).pdf')
tokens = preprocess_and_tokenize(text)

stop_words = set(stopwords.words('english'))

word_tokens = word_tokenize(text)
filtered_text = [w for w in word_tokens if not w in stop_words]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(filtered_text)

print(tokens)
