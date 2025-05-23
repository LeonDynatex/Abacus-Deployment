
import streamlit as st
from onboarding import clone_master_project, create_document_retriever, create_chat_model, create_deployment

st.set_page_config(page_title="School Chatbot Onboarding", layout="centered")

# Initialize session state
if 'project_created' not in st.session_state:
    st.session_state.project_created = False
if 'project_info' not in st.session_state:
    st.session_state.project_info = None

st.title("🎓 School Chatbot Onboarding")

school_name = st.text_input("Enter School Name")

if st.button("🚀 Create Project"):
    if school_name:
        with st.spinner("Setting up your project..."):
            try:
                result = clone_master_project(school_name)
                st.session_state.project_created = True
                st.session_state.project_info = result
                st.success(f"✅ Project created for {school_name}!")
                st.info("Now follow these steps:")
                st.markdown(f"""
                1. Go to [AbacusAI Console](https://console.abacus.ai/projects/{result['project_id']})
                2. Add your data source
                3. Create a feature group named '{school_name}_Knowledge_Base'
                4. Copy the Feature Group ID
                """)
                st.code(result)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("Please enter the school name.")

if st.session_state.project_created and st.session_state.project_info:
    st.divider()
    st.subheader("Manual Steps")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        feature_group_id = st.text_input("Feature Group ID")
        if st.button("1️⃣ Create Document Retriever"):
            if feature_group_id:
                with st.spinner("Creating document retriever..."):
                    try:
                        result = create_document_retriever(
                            st.session_state.project_info["project_id"],
                            st.session_state.project_info["school_name"],
                            feature_group_id
                        )
                        st.session_state.retriever_id = result["retriever_id"]
                        st.success("✅ Document retriever created!")
                        st.code(result)
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("Please enter the Feature Group ID")
    
    with col2:
        if st.button("2️⃣ Create & Train Model"):
            if hasattr(st.session_state, 'retriever_id'):
                with st.spinner("Creating and training model..."):
                    try:
                        result = create_chat_model(
                            st.session_state.project_info["project_id"],
                            st.session_state.project_info["school_name"],
                            st.session_state.retriever_id
                        )
                        st.session_state.model_id = result["model_id"]
                        st.success("✅ Model created and training started!")
                        st.code(result)
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("Please create document retriever first")
    
    with col3:
        if st.button("3️⃣ Create Deployment"):
            if hasattr(st.session_state, 'model_id'):
                with st.spinner("Creating deployment..."):
                    try:
                        result = create_deployment(
                            st.session_state.project_info["project_id"],
                            st.session_state.project_info["school_name"],
                            st.session_state.model_id
                        )
                        st.success("✅ Deployment created!")
                        st.code(result)
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("Please create model first")
