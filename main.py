
import streamlit as st
import abacusai
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('ABACUS_API_KEY')
MASTER_PROJECT_ID = os.getenv('MASTER_PROJECT_ID')

client = abacusai.Client(api_key=API_KEY)

def clone_master_project(master_project_id, new_school_name, gdoc_url):
    new_project = client.create_project(name=f"{new_school_name} Chatbot")
    new_project_id = new_project['projectId']

    dataset = client.create_dataset(
        name=f"{new_school_name} Knowledge Base",
        project_id=new_project_id,
        data_source="GOOGLE_SHEETS",
        data_url=gdoc_url
    )

    master_models = client.list_models(project_id=master_project_id)
    master_model = master_models[0]
    master_model_params = master_model['taskParameters']

    new_model = client.create_model(
        project_id=new_project_id,
        name=f"{new_school_name} Chatbot Model",
        use_case="LLM_AGENT",
        task_type=master_model['taskType'],
        dataset_id=dataset['datasetId'],
        task_parameters=master_model_params
    )

    client.train_model(new_model['modelId'])

    deployment = client.deploy_model(
        model_id=new_model['modelId'],
        name=f"{new_school_name} Deployment"
    )

    return deployment['deploymentId']

st.title("School Chatbot Cloner")

new_school_name = st.text_input("Enter School Name")
gdoc_url = st.text_input("Enter Google Doc URL")

if st.button("Clone Project"):
    if new_school_name and gdoc_url:
        try:
            deployment_id = clone_master_project(MASTER_PROJECT_ID, new_school_name, gdoc_url)
            st.success(f"✅ {new_school_name} cloned. Deployment ID: {deployment_id}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please fill in all fields")
