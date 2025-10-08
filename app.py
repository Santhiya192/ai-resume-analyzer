import streamlit as st
import pandas as pd
from resume_parser import extract_text_from_pdf, preprocess_text, recommend_roles
import spacy

# Load spaCy model (works on local and Streamlit Cloud)
nlp = spacy.load("en_core_web_sm")

# App title
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="centered")
st.title("📄 AI-Powered Resume Analyzer & Job Role Recommender")
st.write("Upload your resume (PDF) and get recommended job roles based on your skills!")

# Upload resume
uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

# Load job roles
try:
    job_data = pd.read_csv("job_roles.csv")
except Exception as e:
    st.error("Could not load job_roles.csv. Make sure the file exists in the repo root.")
    st.stop()

if uploaded_file is not None:
    # Save uploaded file temporarily
    with open("uploaded_resume.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Extract and preprocess text
    resume_text = extract_text_from_pdf("uploaded_resume.pdf")
    if not resume_text.strip():
        st.warning("Could not extract text from this PDF. Using sample text instead.")
        resume_text = "Experienced Python developer skilled in AI, data science, and web development."
    
    processed_text = preprocess_text(resume_text)

else:
    st.info("No file uploaded. Using sample resume text for demo purposes.")
    resume_text = "Experienced Python developer skilled in AI, data science, and web development."
    processed_text = preprocess_text(resume_text)

# Recommend roles
top_matches = recommend_roles(processed_text, job_data)

# Display results
st.subheader("🎯 Top Matching Job Roles")
st.dataframe(top_matches[['Role', 'Match %']])

best_match = top_matches.iloc[0]
st.success(f"✅ Best Match: **{best_match['Role']}** ({best_match['Match %']}% match)")

# Show job descriptions
with st.expander("🔍 View Job Role Descriptions"):
    for i, row in top_matches.iterrows():
        st.markdown(f"**{row['Role']}** — {row['Match %']}% match")
        st.write(row['Description'])
        st.divider()

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using **Python, NLP, and Streamlit**")
