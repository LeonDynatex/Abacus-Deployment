import abacusai

API_KEY = "your_abacus_api_key_here"
MASTER_PROJECT_ID = "your_master_project_id_here"

client = abacusai.AbacusAiClient(api_key=API_KEY)

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

    print(f"✅ {new_school_name} cloned. Deployment ID: {deployment['deploymentId']}")

# Replace with real values
if __name__ == "__main__":
    clone_master_project(
        master_project_id=MASTER_PROJECT_ID,
        new_school_name="School ABC",
        gdoc_url="https://docs.google.com/spreadsheets/d/your-sheet-id-here"
    )
