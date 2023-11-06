import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer



# nltk.download('all')
# nltk.download('stopwords')

def extract_text_from_pdf(file_path):
    pdf_file_obj = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page_obj = pdf_reader.pages[page_num]
        text += page_obj.extract_text()
    pdf_file_obj.close()
    return text

text = extract_text_from_pdf('files/Aero-DWRP_MPA_09.15.22.pdf')

stop_words = set(stopwords.words('english'))

word_tokens = word_tokenize(text)
filtered_text = [w for w in word_tokens if not w in stop_words]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(filtered_text)

print(text)
