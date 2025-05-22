import streamlit as st
from onboarding import clone_master_project

st.set_page_config(page_title="School Chatbot Onboarding", layout="centered")

st.title("🎓 School Chatbot Onboarding")

school_name = st.text_input("Enter School Name")
gdoc_url = st.text_input("Enter Google Doc/Sheet URL")

if st.button("🚀 Onboard School"):
    if school_name and gdoc_url:
        with st.spinner("Setting up your chatbot..."):
            try:
                result = clone_master_project(school_name, gdoc_url)
                st.success(f"✅ {school_name} onboarded successfully!")
                st.code(result)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("Please fill in both fields.")
