import streamlit as st
from PIL import Image
import base64
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import wordnet

# Function to get synonyms of a word
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

# Progress bar using the provided function and styling
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

# LOGO_IMAGE = "PladaAI.png"
LOGO_IMAGE = "pladaainew.png"

img = Image.open('pladaainew.png')
st.set_page_config(
    page_title='PladaAI',
    page_icon=img,
    layout="wide",
)

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

    # Process the uploaded files and remove them from display

    if submit_button:
        if uploaded_files:
            st.write("Uploaded files saved successfully.")
        else:
            st.error('Please upload files to check for plagiarism.')
        
        # uploaded_files = None
elif upload_type == "Upload Text":
    with st.form("text_upload_form"):
        text1 = st.text_area('Enter Your First Text')
        text2 = st.text_area('Enter Your Second Text')
        submit_button = st.form_submit_button("Check for plagiarism")

        # Progress bar initialization
        progress_bar_container = st.empty()

# Inside the if submit_button block
if submit_button:
    if text1 and text2:
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
        st.error("Please enter text to check for plagiarism.")