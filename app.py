import streamlit as st
from resume_reader import extract_text
from utils import split_text
from vector_store import EndeeVectorStore
from qa_model import load_model, answer_question
from skills import extract_skills

# Page config
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)

st.title("🚀 AI Resume Question Answering System")

# Load model once
@st.cache_resource
def load_ai():
    return load_model()

model = load_ai()

# Session state for vector DB
if "vector_db" not in st.session_state:
    st.session_state.vector_db = EndeeVectorStore()

vector_db = st.session_state.vector_db

# Reset button
if st.button("🔄 Reset"):
    st.session_state.vector_db = EndeeVectorStore()
    st.success("Reset successful!")

# Upload resume
uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])

if uploaded_file is not None:

    st.success("✅ Resume uploaded successfully!")

    # Extract text safely
    try:
        resume_text = extract_text(uploaded_file)
    except Exception:
        st.error("❌ Error reading PDF")
        st.stop()

    # Preview
    st.subheader("📄 Resume Preview")
    st.write(resume_text[:1500])

    # Split into chunks
    chunks = split_text(resume_text)

    # Store in vector DB
    with st.spinner("🔍 Indexing resume..."):
        vector_db.add_documents(chunks)

    # Skill extraction
    st.subheader("🧠 Extracted Skills")
    skills = extract_skills(resume_text)

    if skills:
        st.write(", ".join(skills))
    else:
        st.write("No skills detected")

    st.divider()

    # Question answering
    st.subheader("💬 Ask a Question")
    question = st.text_input("Enter your question")

    if st.button("Get Answer"):

        if question.strip() == "":
            st.warning("Please enter a question")
        else:
            results = vector_db.search(question)

            if not results:
                st.warning("No relevant information found.")
            else:
                context = " ".join(results)

                answer = answer_question(model, context, question)

                st.subheader("📌 Answer")
                st.write(answer)

                with st.expander("🔎 Retrieved Resume Context"):
                    for r in results:
                        st.write("-", r)

else:
    st.info("📄 Please upload a resume PDF to begin.")