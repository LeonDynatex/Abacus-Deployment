import abacusai
import os
from dotenv import load_dotenv

load_dotenv()
client = abacusai.ApiClient(api_key=os.getenv("ABACUS_API_KEY"))
MASTER_PROJECT_ID = os.getenv("MASTER_PROJECT_ID")

def clone_master_project(new_school_name):
    try:
        # Create new project
        print(f"Creating project for {new_school_name}...")
        new_project = client.create_project(
            name=f"{new_school_name} Chatbot",
            use_case="CHAT_LLM"
        )
        new_project_id = new_project.project_id
        print(f"✅ Created project: {new_project_id}")

        # Get master project configuration
        print("Getting master project configuration...")
        master_models = client.list_models(project_id=MASTER_PROJECT_ID)
        if not master_models:
            raise ValueError("No models found in master project")

        master_model = master_models[0]
        print(f"✅ Found master model: {master_model.model_id}")

        # Get master project's feature groups/datasets
        try:
            master_feature_groups = client.list_feature_groups(project_id=MASTER_PROJECT_ID)
            print(f"Master project has {len(master_feature_groups)} feature groups")
        except:
            master_feature_groups = []
            print("Could not list master feature groups")

        # 3. Manual dataset setup instructions
        print(f"\n⚠️  MANUAL STEP REQUIRED:")
        print(f"1. Go to https://console.abacus.ai/projects/{new_project_id}")
        print(f"2. Create a feature group named '{new_school_name} Knowledge Base'")
        print(f"3. Note down the feature group ID to continue setup")

        # Store project info for later use
        global current_project_info
        current_project_info = {
            "project_id": new_project_id,
            "school_name": new_school_name,
            "master_model": master_model
        }

        return {
            "project_id": new_project_id,
            "school_name": new_school_name,
            "status": "project_created",
            "next_steps": "Add dataset manually, then call create_document_retriever(project_id, school_name, feature_group_id)"
        }

    except Exception as e:
        print(f"❌ Error in clone_master_project: {str(e)}")
        raise

def create_document_retriever(project_id, school_name, feature_group_id):
    try:
        retriever = client.create_document_retriever(
            name=f"{school_name}_Document_Retriever",
            project_id=project_id,
            feature_group_id=feature_group_id
        )
        print(f"✅ Created document retriever: {retriever.document_retriever_id}")
        return {
            "retriever_id": retriever.document_retriever_id,
            "status": "retriever_created",
            "next_steps": "Call create_chat_model(project_id, school_name, retriever_id)"
        }
    except Exception as e:
        print(f"❌ Error creating document retriever: {str(e)}")
        raise

def create_chat_model(project_id, school_name, retriever_id):
    try:
        model = client.create_llm_model(
            name=f"{school_name}_Chatbot_Model",
            project_id=project_id,
            document_retriever_ids=[retriever_id]
        )
        print(f"✅ Created model: {model.model_id}")
        client.train_model(model.model_id)
        print(f"✅ Training started for model: {model.model_id}")
        return {
            "model_id": model.model_id,
            "status": "model_created_and_training",
            "next_steps": "Call create_deployment(project_id, school_name, model_id)"
        }
    except Exception as e:
        print(f"❌ Error creating/training model: {str(e)}")
        raise

def create_deployment(project_id, school_name, model_id):
    try:
        deployment = client.create_chat_deployment(
            model_id=model_id,
            name=f"{school_name}_Deployment",
            project_id=project_id
        )
        deployment_id = getattr(deployment, 'deployment_id', 
                                  getattr(deployment, 'id', None))
        print(f"✅ Created deployment: {deployment_id}")
        return {
            "deployment_id": deployment_id,
            "status": "deployment_created"
        }
    except Exception as e:
        print(f"❌ Error creating deployment: {str(e)}")
        raise

def quick_clone_with_manual_steps(new_school_name, gdoc_url):
    """One-step function that provides manual instructions"""
    try:
        # Create project
        result = clone_master_project(new_school_name)
        project_id = result["project_id"]
        print(f"\n" + "="*60)
        print(f"🎯 SETUP INSTRUCTIONS FOR {new_school_name.upper()}")
        print(f"="*60)
        print(f"1. Go to: https://console.abacus.ai/projects/{project_id}")
        print(f"2. Click 'Add Data Source'")
        print(f"3. Choose 'Google Sheets' and enter: {gdoc_url}")
        print(f"4. Name it: '{new_school_name} Knowledge Base'")
        print(f"5. After creation, copy the Feature Group ID")
        print(f"6. Run: create_document_retriever(project_id, school_name, 'your_feature_group_id')")
        print(f"="*60)

        return result

    except Exception as e:
        print(f"❌ Setup failed: {str(e)}")
        raise

# Example usage:
# result = quick_clone_with_manual_steps("Example School", "https://docs.google.com/spreadsheets/d/your-sheet-id")
# Then after manual dataset creation:
# final_result = create_document_retriever(project_id, school_name, "your_feature_group_id_here")