
import streamlit as st
from onboarding import clone_master_project, continue_setup

st.set_page_config(page_title="School Chatbot Onboarding", layout="centered")

st.title("🎓 School Chatbot Onboarding")

tab1, tab2 = st.tabs(["Initial Setup", "Continue Setup"])

with tab1:
    school_name = st.text_input("Enter School Name")
    gdoc_url = st.text_input("Enter Google Doc/Sheet URL")

    if st.button("🚀 Start Onboarding"):
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

with tab2:
    feature_group_id = st.text_input("Enter Feature Group ID")
    
    if st.button("▶️ Continue Setup"):
        if feature_group_id:
            with st.spinner("Continuing setup..."):
                try:
                    result = continue_setup(feature_group_id)
                    st.success("✅ Setup continued successfully!")
                    st.code(result)
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("Please enter the Feature Group ID.")
