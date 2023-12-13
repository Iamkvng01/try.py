import streamlit as st
from PIL import Image

img = Image.open('PladaAI.png')
st.set_page_config(
    page_title='PladaAI',
    page_icon=img,
    layout="wide",
)

# st.markdown(
#     """
#     <style>
# MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# header {visibility: hidden;}
# </style>
# """,
# unsafe_allow_html=True
# )




#first paragraph and image
st.header('What is Plagiarism?')
img = Image.open('jap.jpeg')
new_img = img.resize((520,220), Image.Resampling.BILINEAR)

col1,col2 = st.columns([1,1])
with col1:
    st.image(new_img)
    with col2:
        st.markdown('<div style="text-align: justify; text-align: left;">Plagiarism is the unethical and dishonest act of using someone else words, ideas, or data as your own without giving credit to the original source. It can be intentional or unintentional, and can take many forms, such as copying and pasting text without quotation marks and citation, paraphrasing or summarizing someone elses work without citation, using images, graphs, charts, or other visual elements without permission or citation and submitting or publishing someone else’s work as your own or reusing your own work without disclosure.</div>', unsafe_allow_html=True)

#second paragraph 
st.header('Why is Plagiarism wrong?')
image = Image.open('pla_wrong.png')
col1 , col2 = st.columns([1,1])
with col1:
    st.markdown('<div style="text-align: justify;">Plagiarism is wrong because it violates the intellectual property rights of the original author or creator, and it also undermines the academic integrity and professional standards of your field or industry. If you are caught plagiarizing, you may face serious consequences such as losing marks, grades or credits for your assignment or course, or disciplinary action from your school, college, or university, loss of reputation, trust or respect among your peers, colleagues, or clients, legal action from copyright holder or the publisher and damage to your career prospects, opportunities, or advancement.</div>' , unsafe_allow_html=True)
with col2:
    st.image(image)
 
 #Third paragraph and image   
st.header('How to avoid Plagiarism?')
imagew = Image.open('avoidplag.jpeg')
new_imagew = image.resize((520,300), Image.Resampling.BILINEAR)
col1,col2 = st.columns([1,1])
with col1:
    st.markdown('<div style="text-align: justify;">To avoid plagiarism, it is essential to acknowledge and cite your sources properly. Depending</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: justify;">on your field or industry, you can use various citation styles, such as APA, MLA or Chicago.</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: justify;">Additionally, you can use online tools such as plagiarism checkers, citation generators, or paraphrasing software, to help you with your writing. However, it is important to use your own critical thinking, analysis, and creativity to produce original and quality work.</div>' , unsafe_allow_html=True)
with col2:
    st.image(imagew)
    
st.title('Here are some tips to help you avoid plagiarism')
st.write('i.Plan your research and writing ahead of time and keep track of your sources and notes.')
st.write('ii.Quote directly from your sources when you want to use their exact words and use quotation marks and citation.')
st.write('iii.Paraphrase or summarize your sources when you want to use their ideas and use your own words and voice and citation.')
st.write('iv.Compare your work with your sources and make sure you have not copied or paraphrased too closely.')
st.write('v.Cite your sources correctly and consistently according to the citation style and format required by your field or industry.')
st.write('vi.Check your work for plagiarism using a reliable plagiarism checker before submitting or publishing it.')

st.header('How to deal with Plagiarism?')
pic = Image.open('last.jpeg')
new_pic = pic.resize((350,150), Image.Resampling.BILINEAR)

col1,col2 = st.columns([1,1])
with col1:
     st.markdown('<div style="text-align: justify;">If you suspect or discover that someone has plagiarized your work, you should take action to protect your rights and reputation. You can contact the person to remove it, correct it or cite it properly. Additionally, you can contact the publisher, editor, or platform where the plagiarized work is published and request them to take it down, edit it or add a citation. If the plagiarism involves a student or faculty member, you should contact your school, college or university and report the incident to the relevant authority or committee. Lastly, if the plagiarism involves a serious breach of copyright or a potential lawsuit, you should contact a lawyer or a legal advisor.</div>', unsafe_allow_html=True)
with col2:
     st.image(new_pic)
    


link = Image.open('linked.png')
new_link = link.resize((25,25), Image.Resampling.BILINEAR)

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
        col1, col2 = st.columns([1,1])
        with col1:
            st.write('Privacy Policy')
        with col2:
            st.image(new_link)

    with col3:
        st.markdown('Designed by Datascience stack')