import streamlit as st
from PIL import Image
import base64
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import wordnet
from itertools import combinations
from io import BytesIO
import docx2txt 
import PyPDF2
import os



LOGO_IMAGE = "pladaainew.png"
img = Image.open('pladaainew.png')
st.set_page_config(
    page_title='PladaAI',
    page_icon=img,
    layout="wide",
)


def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    words = nltk.word_tokenize(text.lower())
    words = [word for word in words if word.isalnum() and word not in stop_words]
    return ' '.join(words)

from tempfile import NamedTemporaryFile

import fitz # PyMuPDF library

def extract_text_from_pdf(uploaded_file):
    try:
        # Save the uploaded file to a temporary location
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            file_path = temp_file.name

        # Process the PDF file using PyMuPDF
        with fitz.open(file_path) as pdf_document:
            text = ""
            for page_number in range(pdf_document.page_count):
                page = pdf_document[page_number]
                text += page.get_text()

        return text

    finally:
        # Clean up: Remove the temporary file
        if file_path:
            os.remove(file_path)

def extract_text_from_docx(file):
    return docx2txt.process(file)

def extract_text_from_txt(file):
    return file.getvalue().decode("utf-8")

def compute_similarity(doc1, doc2, vectorizer):
    vectorized_docs = vectorizer.transform([doc1, doc2])
    similarity = cosine_similarity(vectorized_docs)
    return similarity[0, 1]

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)

# Function to expand text with synonyms
def expand_with_synonyms(text):
    words = nltk.word_tokenize(text)
    expanded_text = []
    for word in words:
        expanded_text.extend(get_synonyms(word))
    return ' '.join(expanded_text)

def update_progress(percentage):
    if percentage < 16:
        color = "green"
    elif 16 <= percentage < 35:
        color = "yellow"
    else:
        color = "red"
    
    st.markdown(f"""
        <style>
            .custom-progress-container {{
                width: 100%;
                background-color: #eee;
                border-radius: 10px;
                padding: 5px;
            }}
            .custom-progress-bar {{
                width: {percentage}%;
                height: 25px;
                border-radius: 10px;
                background-color: {color};
                text-align: center;
                line-height: 25px;
                color: black;
            }}
        </style>
        <div class="custom-progress-container">
            <div class="custom-progress-bar">{percentage}%</div>
        </div>
    """, unsafe_allow_html=True)


st.markdown(
    """
    <style>
    body {
            margin: 0;
            padding: 0;
    }
    
    .logo-text {
        font-weight: 500
        font-size: 30px !important;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .logotext{
        font-weight: 800 !important;
        font-size: 25px !important;
        text-align: center;
        margin-bottom: 10px;
        margin-left: -30px;
        
    }
    
    # MainMenu {visibility: hidden;}
    # footer {visibility: hidden;}
    # header {visibility: hidden;}
  
    .container {
        display: flex;
        align-items: center; /* Align items vertically in the container */
        justify-content: center; /* Align items horizontally in the container */
        gap: 0px; /* Add a gap between the image and text */
    }  
    .logo-img {
        width: 200px; /* Set width for the image */
        height: 200px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()} ">
        <p class="logotext">Welcome to Plada AI</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
        """
        <h4 class="logo-text">
            How can I help you today?
        </h4>
        """,
        unsafe_allow_html=True
    )

    
st.markdown("\n\n")
st.markdown("\n\n")
st.markdown("\n\n")

# User instructions
st.markdown(
    """
    ### User Instructions:
    1. Choose the upload type.
    2. If you select "Upload File," you can upload one or more files, and then click the button below.
    3. If you select "Upload Text," enter your text in the provided text areas and click the button below.
    4. The results will be displayed below.
    """
)

upload_type = st.radio("Select upload type", ("Upload File", "Upload Text"))
if upload_type == "Upload File":
    with st.form("File Upload"):
        uploaded_files = st.file_uploader(accept_multiple_files=True, label='Upload your files here to check for plagiarism')
        submit_button = st.form_submit_button("Check for plagiarism")

        threshold_percentage = st.slider('Select similarity Threshold (%)', 0, 100)
        
        # Process the uploaded files and remove them from display
        if submit_button and uploaded_files:
            st.subheader("Document Similarities:")
            
            documents = []
            document_names = []
            
            for file in uploaded_files:
                file_extension = file.name.split('.')[-1].lower()
                document_names.append(file.name)

                if file_extension == 'pdf':
                    text = extract_text_from_pdf(file)
                elif file_extension == 'txt':
                    text = extract_text_from_txt(file)
                elif file_extension == 'docx':
                    text = extract_text_from_docx(BytesIO(file.read()))
                else:
                    st.warning(f"Unsupported file format: {file_extension}")
                    continue

                documents.append(preprocess_text(text))

            vectorizer = TfidfVectorizer()
            vectorized_documents = vectorizer.fit_transform(documents)

            doc_pairs = list(combinations(range(len(documents)), 2))
            for pair in doc_pairs:
                doc1, doc2 = pair
                similarity = compute_similarity(documents[doc1], documents[doc2], vectorizer
                )
                if similarity * 100 >= threshold_percentage or threshold_percentage == 0:
                    st.write(f"Similarity between Document {document_names[doc1]} and Document {document_names[doc2]} is: {int(similarity*100)}%")


elif upload_type == "Upload Text":
    with st.form("text_upload_form"):
        text1 = st.text_area('Enter Your First Text')
        text2 = st.text_area('Enter Your Second Text')
        submit_button = st.form_submit_button("Check for plagiarism")

        # Progress bar initialization
        progress_bar_container = st.empty()

        if submit_button and text1 and text2:
            # Combine texts
            preprocessed_docs = [text1, text2]

            # Expand vocabulary with synonyms
            expanded_docs = [expand_with_synonyms(doc) for doc in preprocessed_docs]

            # Compute TF-IDF with n-grams
            tfidf_vectorizer = TfidfVectorizer(tokenizer=nltk.word_tokenize, stop_words='english', ngram_range=(1, 3))
            tfidf_matrix = tfidf_vectorizer.fit_transform(expanded_docs)

            # Compute cosine similarity
            similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
            similarity = similarity_matrix[0, 1]

            # Update progress bar value based on similarity
            progress_value = int(similarity * 100)

            # Display custom progress bar
            update_progress(progress_value)

            # Check if there is a similarity, then display the percentage
            if similarity > 0:
                st.write(f"Percentage of similarity between the two texts: {int(similarity*100)}")
            else:
                st.write("No similarity found between the two texts.")
        else:
            st.warning("Please enter text to check for plagiarism.")
            
# Footer
link = Image.open('linked.png')
new_link = link.resize((25, 25), Image.Resampling.BILINEAR)



st.markdown('<hr>', unsafe_allow_html=True)
footer_container = st.container()

footer_style = """
    <style>
        .stFooter {
            position: fixed;
            bottom: 0;
            width: 100%;
        }
    </style>
"""
st.markdown(footer_style, unsafe_allow_html=True)

with footer_container:
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown("&copy; 2023 Nhub. All rights reserved.", unsafe_allow_html=True)

    with col2:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.write('Privacy Policy')
        with col2:
           st.image(new_link)

    with col3:
        st.markdown('Designed by Datascience stack')


footer_style = """
    <style>
        .stFooter {
            position: fixed;
            bottom: 0;
            width: 100%;
        }
    </style>
"""
