import json
import requests
from requests.exceptions import RequestException
import streamlit as st
from streamlit_lottie import st_lottie
import base64
from PIL import Image
import nltk
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ssl

# Progress bar using the provided function and styling
def update_progress(percentage):
    if percentage < 16:
        color = "green"
    elif 16 <= percentage < 35:
        color = "yellow"
    else:
        color = "red"

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
    MainMenu {visibility: hidden}
    footer {visibility: hidden}
    header {visibility: hidden}
    </style>
    """,
    unsafe_allow_html=True
)

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"jpeg"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
add_bg_from_local('bg.jpeg')

def load_lottiefile(filepath: str):
    with open(filepath, 'r') as f:
        return json.load(f)

col1, col2 = st.columns(2)
with col1:
    image = Image.open('bg.jpeg')
    st.markdown(
        """
        <style>
        .big-font {{
            font-size: 70px !important;
            font-family: 'Sans serif';
            font-weight: 300;
            color:
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<h2 class="big-font">PladaAI</h2>', unsafe_allow_html=True)

with col2:
    st.markdown("<h3 style='text-align: justify;'> PladaAI is a comprehensive software solution designed to help academic institutions maintain the integrity of their educational programs by identifying and preventing plagiarism among students</h3>", unsafe_allow_html=True)
    upload_type = "Upload Text"
    with st.form("text_upload_form"):
        text1 = st.text_area('Enter Your First Text')
        text2 = st.text_area('Enter Your Second Text')
        submit_button = st.form_submit_button("Check for plagiarism")
    if submit_button:
        if text1 and text2:
            try:
                _create_unverified_https_context = ssl._create_unverified_context
            except AttributeError:
                pass
            else:
                ssl._create_default_https_context = _create_unverified_https_context

            def get_synonyms(word):
                synonyms = set()
                for syn in wordnet.synsets(word):
                    for lemma in syn.lemmas():
                        synonyms.add(lemma.name())
                return list(synonyms)

            def expand_with_synonyms(text):
                words = nltk.word_tokenize(text)
                expanded_text = []
                for word in words:
                    expanded_text.extend(get_synonyms(word))
                return ' '.join(expanded_text)

            def calculate_similarity(text1, text2):
                if not text1 or not text2:
                    st.error("Please enter valid texts.")
                    return

                preprocessed_docs = [text1, text2]
                expanded_docs = [expand_with_synonyms(doc) for doc in preprocessed_docs]
                tfidf_vectorizer = TfidfVectorizer(tokenizer=nltk.word_tokenize, stop_words='english', ngram_range=(1, 3))
                tfidf_matrix = tfidf_vectorizer.fit_transform(expanded_docs)
                similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
                similarity = similarity_matrix[0, 1]
                
                # Display similarity in a progress bar with red color
                progress_bar = st.progress(0)
                for percent_complete in range(0, int(similarity * 100) + 1, 10):
                    progress_bar.progress(percent_complete / 100.0)

                st.success(f"Percentage of similarity between the two texts: {similarity:.3%}")

            calculate_similarity(text1, text2)

        else:
            st.error("Please enter text to check for plagiarism.")
    st.link_button('Get Started', 'http://localhost:8505/', use_container_width=True)

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
st.markdown(footer_style, unsafe_allow_html=True)