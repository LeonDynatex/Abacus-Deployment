import streamlit as st
from onboarding import setup_new_school_project, create_document_retriever, quick_setup_with_checklist
 
st.set_page_config(page_title="School Chatbot Onboarding", layout="centered")

# Initialize session state
if 'project_created' not in st.session_state:
    st.session_state.project_created = False
if 'project_info' not in st.session_state:
    st.session_state.project_info = None
if 'retriever_created' not in st.session_state:
    st.session_state.retriever_created = False
if 'model_trained' not in st.session_state:
    st.session_state.model_trained = False
if 'deployment_created' not in st.session_state:
    st.session_state.deployment_created = False

st.title("🎓 School Chatbot Onboarding")

# Step 1: Project Creation
st.header("Step 1: Create Project")

school_name = st.text_input("Enter School Name")

if st.button("🚀 Create Project"):
    if school_name:
        with st.spinner("Setting up your project..."):
            try:
                result = setup_new_school_project(school_name)
                st.session_state.project_created = True
                st.session_state.project_info = result
                st.success(f"✅ Project created for {school_name}!")
                
                # Display manual instructions
                st.info("📋 **Manual Step Required:**")
                st.markdown(f"""
                1. Go to [AbacusAI Console](https://console.abacus.ai/projects/{result['project_id']})
                2. Click **'Add Data Source'**
                3. Choose your data source type (Google Sheets, CSV, etc.)
                4. Name it: **'{school_name} Knowledge Base'**
                5. Click **'Create Feature Group'**
                6. Copy the **Feature Group ID** and paste it below
                """)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("Please enter the school name.")

# Step 2: Document Retriever Creation
if st.session_state.project_created and st.session_state.project_info:
    st.divider()
    st.header("Step 2: Create Document Retriever")
    
    feature_group_id = st.text_input("📋 Feature Group ID (from Abacus Console)")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        data_source_completed = st.checkbox("✅ I have completed the data source setup above")
    
    with col2:
        if st.button("🔗 Create Document Retriever", disabled=not data_source_completed):
            if feature_group_id:
                with st.spinner("Creating document retriever..."):
                    try:
                        result = create_document_retriever(
                            st.session_state.project_info["project_id"],
                            st.session_state.project_info["school_name"],
                            feature_group_id
                        )
                        st.session_state.retriever_created = True
                        st.session_state.retriever_id = result["retriever_id"]
                        st.success("✅ Document retriever created!")
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("Please enter the Feature Group ID")

# Step 3: Manual Training Instructions
if st.session_state.retriever_created:
    st.divider()
    st.header("Step 3: Create & Train Model (Manual)")
    
    st.info("📋 **Manual Steps Required in Abacus Console:**")
    st.markdown(f"""
    1. Go to [AbacusAI Console](https://console.abacus.ai/projects/{st.session_state.project_info['project_id']})
    2. Click **'Create Model'**
    3. Select **'Chat LLM'** use case
    4. Name: **'{st.session_state.project_info['school_name']}_Chatbot_Model'**
    5. Select your document retriever: `{st.session_state.retriever_id}`
    6. Click **'Create Model'**
    7. Click **'Train Model'**
    8. Wait for training to complete
    """)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        model_trained = st.checkbox("✅ Model training is complete")
        if model_trained:
            st.session_state.model_trained = True
    
    with col2:
        if st.session_state.model_trained:
            st.success("Ready for deployment!")

# Step 4: Manual Deployment Instructions
if st.session_state.model_trained:
    st.divider()
    st.header("Step 4: Create Deployment (Manual)")
    
    st.info("📋 **Final Manual Steps:**")
    st.markdown(f"""
    1. In the Abacus Console, after training completes
    2. Click **'Deploy Model'**
    3. Name: **'{st.session_state.project_info['school_name']}_Deployment'**
    4. Configure deployment settings as needed
    5. Click **'Create Deployment'**
    """)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        deployment_created = st.checkbox("✅ Deployment is live")
        if deployment_created:
            st.session_state.deployment_created = True
    
    with col2:
        if st.session_state.deployment_created:
            st.success("🎉 Setup Complete!")

# Progress Summary
if st.session_state.project_created:
    st.divider()
    st.header("📊 Setup Progress")
    
    progress_steps = [
        ("Project Created", st.session_state.project_created),
        ("Document Retriever Created", st.session_state.retriever_created),
        ("Model Trained", st.session_state.model_trained),
        ("Deployment Created", st.session_state.deployment_created)
    ]
    
    completed_steps = sum(1 for _, completed in progress_steps if completed)
    progress_percentage = (completed_steps / len(progress_steps)) * 100
    
    st.progress(progress_percentage / 100)
    st.write(f"Progress: {completed_steps}/{len(progress_steps)} steps completed ({progress_percentage:.0f}%)")
    
    # Show checklist
    for step_name, completed in progress_steps:
        if completed:
            st.write(f"✅ {step_name}")
        else:
            st.write(f"⏳ {step_name}")
    
    if st.session_state.deployment_created:
        st.balloons()
        st.success(f"🎉 Congratulations! Your {st.session_state.project_info['school_name']} chatbot is now live and ready to use!")

# Reset button (for testing)
st.divider()
if st.button("🔄 Reset Setup", type="secondary"):
    for key in ['project_created', 'project_info', 'retriever_created', 'model_trained', 'deployment_created']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()
