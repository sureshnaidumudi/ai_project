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

# Upload resume
uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])

# Load AI model
@st.cache_resource
def load_ai():
    return load_model()

model = load_ai()

# Initialize vector DB
vector_db = EndeeVectorStore()

if uploaded_file is not None:

    st.success("✅ Resume uploaded successfully!")

    # Extract text
    resume_text = extract_text(uploaded_file)

    # Show preview
    st.subheader("📄 Resume Preview")
    st.write(resume_text[:1500])

    # Split resume into chunks
    chunks = split_text(resume_text)

    # Store into vector database
    vector_db.add_documents(chunks)

    # Extract skills
    st.subheader("🧠 Extracted Skills")
    skills = extract_skills(resume_text)

    if skills:
        st.write(", ".join(skills))
    else:
        st.write("No skills detected")

    st.divider()

    # Ask question section
    st.subheader("💬 Ask a Question")

    question = st.text_input("Enter your question")

    if st.button("Get Answer"):

        if question.strip() == "":
            st.warning("Please enter a question")
        else:

            # Search relevant chunks
            results = vector_db.search(question)

            if not results:
                st.warning("No relevant information found.")
            else:
                context = " ".join(results)

                # Generate answer
                answer = answer_question(model, context, question)

                st.subheader("📌 Answer")
                st.write(answer)

                # Show retrieved context
                with st.expander("🔎 Retrieved Resume Context"):
                    for r in results:
                        st.write("-", r)

else:
    st.info("📄 Please upload a resume PDF to begin.")