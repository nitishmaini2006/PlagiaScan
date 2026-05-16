import streamlit as st
from difflib import SequenceMatcher
from docx import Document
from PyPDF2 import PdfReader

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="PlagiaScan",
    page_icon="🛡️",
    layout="centered"
)

# ---------------- STYLING ---------------- #

st.markdown("""
<style>
.big-title {
    font-size: 50px;
    font-weight: bold;
    color: white;
}

.subtitle {
    font-size: 22px;
    color: #b0b0b0;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #

st.markdown('<p class="big-title">🛡️ PlagiaScan</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI Powered Text Similarity Detector</p>', unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("📌 About")

st.sidebar.info("""
Supports:
- TXT files
- PDF files
- DOCX files

Built using:
- Python
- Streamlit
- PyPDF2
- python-docx
""")

# ---------------- FILE READING FUNCTIONS ---------------- #

def read_txt(file):
    return file.read().decode("utf-8")

def read_docx(file):
    doc = Document(file)
    text = []

    for para in doc.paragraphs:
        text.append(para.text)

    return "\n".join(text)

def read_pdf(file):
    pdf = PdfReader(file)
    text = ""

    for page in pdf.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text

def extract_text(file):

    if file.name.endswith(".txt"):
        return read_txt(file)

    elif file.name.endswith(".docx"):
        return read_docx(file)

    elif file.name.endswith(".pdf"):
        return read_pdf(file)

    else:
        return ""

# ---------------- FILE UPLOAD ---------------- #

file1 = st.file_uploader(
    "📄 Upload First File",
    type=["txt", "pdf", "docx"]
)

file2 = st.file_uploader(
    "📄 Upload Second File",
    type=["txt", "pdf", "docx"]
)

# ---------------- MAIN LOGIC ---------------- #

if file1 and file2:

    text1 = extract_text(file1)
    text2 = extract_text(file2)

    similarity = SequenceMatcher(None, text1, text2).ratio()

    percentage = similarity * 100

    st.divider()

    st.markdown("## 📊 Analysis Result")

    st.success(f"✅ Similarity Score: {percentage:.2f}%")

    st.progress(similarity)

    # Similarity warnings
    if percentage > 80:
        st.error("⚠️ High Similarity Detected")

    elif percentage > 50:
        st.warning("⚠️ Moderate Similarity")

    else:
        st.info("✅ Low Similarity")

    # Expandable preview
    with st.expander("📄 Show Extracted Text"):

        st.subheader("First File")
        st.write(text1[:5000])

        st.subheader("Second File")
        st.write(text2[:5000])