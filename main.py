
import streamlit as st
from onboarding import clone_master_project, continue_setup

st.set_page_config(page_title="School Chatbot Onboarding", layout="centered")

st.title("🎓 School Chatbot Onboarding")

tab1, tab2 = st.tabs(["Initial Setup", "Continue Setup"])

with tab1:
    school_name = st.text_input("Enter School Name")

    if st.button("🚀 Start Project Setup"):
        if school_name:
            with st.spinner("Setting up your project..."):
                try:
                    result = clone_master_project(school_name)
                    st.success(f"✅ Project created for {school_name}!")
                    st.info("Now follow these steps:")
                    st.markdown(f"""
                    1. Go to [AbacusAI Console](https://console.abacus.ai/projects/{result['project_id']})
                    2. Add your data source
                    3. Create a feature group named '{school_name} Knowledge Base'
                    4. Copy the Feature Group ID
                    5. Return here and use the 'Continue Setup' tab to complete the setup
                    """)
                    st.code(result)
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("Please enter the school name.")

with tab2:
    feature_group_id = st.text_input("Enter Feature Group ID")
    
    if st.button("▶️ Continue Setup"):
        if feature_group_id:
            with st.spinner("Continuing setup..."):
                try:
                    result = continue_setup(feature_group_id)
                    st.success("✅ Setup completed successfully!")
                    st.code(result)
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("Please enter the Feature Group ID.")
