import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import base64
from PIL import Image
from nltk.corpus import stopwords
import json 
import sqlite3
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from itertools import combinations
from io import BytesIO
import docx2txt 
import PyPDF2
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ssl
import streamlit_authenticator as stauth

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

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    words = nltk.word_tokenize(text.lower())
    words = [word for word in words if word.isalnum() and word not in stop_words]
    return ' '.join(words)

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfFileReader(file)
    text = ''
    for page_num in range(pdf_reader.numPages):
        text += pdf_reader.getPage(page_num).extractText()
    return text

def extract_text_from_docx(file):
    return docx2txt.process(file)

def extract_text_from_txt(file):
    return file.getvalue().decode("utf-8")

def compute_similarity(doc1, doc2, vectorizer):
    vectorized_docs = vectorizer.transform([doc1, doc2])
    similarity = cosine_similarity(vectorized_docs)
    return similarity[0, 1]

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

# DB Management
conn = sqlite3.connect('data1.db')
c = conn.cursor()

# Function to create a table
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT, email TEXT)')

def add_userdata(username, password, email):
    c.execute('INSERT INTO userstable(username, password, email) VALUES (?, ?, ?)', (username, password, email))
    conn.commit()

# Fun to login
def login_user(email,password):
    c.execute('SELECT * FROM userstable WHERE email = ? AND password = ? ', (email,password))
    data = c.fetchall()
    return data

# Function to get or create SessionState
def get_session_state():
    return st.session_state

# Get or create the session state
ss = get_session_state()

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
    .logo-img {
        width: 200px; /* Set width for the image */
        height: 200px;
        margin-bottom: -20px;
        margin-left: -50px;
        text-align: ;
    }
    # MainMenu {visibility: hidden;}
    # footer {visibility: hidden;}
    # header {visibility: hidden;}
    
    .logotext{
        font-weight: 800 !important;
        font-size: 25px !important;
        text-align: center;
        margin-bottom: 10px;
        margin-left: -30px;
    }
   .logotext{
        font-weight: 800 !important;
        font-size: 25px !important;
        text-align: center;
        margin-top: -105px;
        margin-left: -300px;
        
    }
    .ani1{
        font-weight: 5600;
        font-size: 25px;
        text-align: left;
        margin-top: 25px;
        margin-left: -240px;
    }
    .ani2{
        font-weight: 5600;
        font-size: 25px;
        text-align: left;
        margin-top: 64px;
        margin-left: -240px;
    }
    </style>
""",
    unsafe_allow_html=True
)

def load_lottiefile(filepath: str):
    with open(filepath, 'r') as f:
        return json.load(f)
    
col3, col4 = st.columns([2,1])
   
with st.sidebar:
        st.markdown(
            f"""
            <div class="container">
                <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()} "> 
                
            </div>
            """,
            unsafe_allow_html=True
        )
        st.subheader('Get Started')
        
        selected = option_menu(
            menu_title=None,
            options=['Login', 'Signup'],
            default_index=0
        )

        if selected == 'Login':
            ss.login_button_pressed = True
            ss.signup_button_pressed = False

            st.subheader('Login')
            email = st.text_input('Enter your email: ')
            password = st.text_input('Enter your password: ', type='password')

            if st.button('Login', 'main'):
                create_usertable()
                result = login_user(email, password)
            
                if result:
                    st.success('Logged in as {}'.format(email))

                else:
                    st.error('Wrong username or password')

        if selected == 'Signup':
            ss.signup_button_pressed = True
            ss.login_button_pressed = False

            
            st.subheader('Sign Up')
            name = st.text_input('Enter Full Name: ')
            sign_username = st.text_input("Enter your Username: ")
            st.error('Password must contain at least 1 uppercase, 1 lowercase, 1 special character and at least 8 characters long!')
            sign_password = st.text_input('Create your Password: ', type='password')
            con_password = st.text_input('Confirm your password: ', type='password')
            email = st.text_input('Enter your Email:')
            if st.button('Submit'):
                c.execute('SELECT * FROM userstable WHERE username = ? OR email = ?', (sign_username, email))
                existing_user = c.fetchall()

                if existing_user:
                    st.error('User already exists. Please login or use different credentials.')
                else:
                    if sign_password == con_password:  # Check if passwords match
                        if len(sign_password) >= 8:  # Check password length

                            # Regex pattern to validate password
                            pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\W)')
                            if pattern.match(sign_password):
                                create_usertable()
                                add_userdata(sign_username, sign_password, email)
                                st.success('Successfully signed up!')
                            else:
                                st.error('Password must contain at least 1 uppercase, 1 lowercase, and 1 special character.')
                        else:
                            st.error('Password should be at least 8 characters long!')
                    else:
                        st.error('Passwords do not match!')


col2_1, col2_2 = st.columns([1,1])
with col2_1:
        # For FilePath
        lottie_coding = load_lottiefile('welcome.json')
        st_lottie(lottie_coding,
              speed=1,
              reverse=False,
              loop=True,
              height=110,
              width=110,
              key='wellcome')
        
with col2_2:
        st.markdown(
            f"""
            <div> 

            <h5 style = 'text-align: justify;' class="ani1">PladaAI is an advanced educational software combating plagiarism in academic settings. Tailored for educators, it detects and prevents plagiarism, ensuring academic integrity. By fostering originality, it safeguards educational standards, nurturing a culture of honesty and innovation.</h5>

            </div>
            """,
            unsafe_allow_html=True
        )


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

with st.form('Text Upload From'):
    text1 = st.text_area('Enter Your First Text')
    text2 = st.text_area('Enter Your Second Text')
    submit_button = st.form_submit_button('Check For Plagiarism')

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