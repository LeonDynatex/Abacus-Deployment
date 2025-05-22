import abacusai
import os
from dotenv import load_dotenv

load_dotenv()
client = abacusai.ApiClient(api_key=os.getenv("ABACUS_API_KEY"))
MASTER_PROJECT_ID = os.getenv("MASTER_PROJECT_ID")

def clone_master_project(new_school_name, gdoc_url):
    try:
        # 1. Create new project
        print(f"Creating project for {new_school_name}...")
        new_project = client.create_project(
            name=f"{new_school_name} Chatbot",
            use_case="CHAT_LLM"
        )
        new_project_id = new_project.project_id
        print(f"✅ Created project: {new_project_id}")

        # 2. Get master project configuration
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
        print(f"Since automatic dataset creation failed, please:")
        print(f"1. Go to https://console.abacus.ai/projects/{new_project_id}")
        print(f"2. Add your Google Sheets data source: {gdoc_url}")
        print(f"3. Create a feature group named '{new_school_name} Knowledge Base'")
        print(f"4. Note down the feature group ID and run: set_feature_group_id('your_feature_group_id')")

        # Store project info for later use
        global current_project_info
        current_project_info = {
            "project_id": new_project_id,
            "school_name": new_school_name,
            "master_model": master_model,
            "gdoc_url": gdoc_url
        }

        return {
            "project_id": new_project_id,
            "status": "project_created_dataset_manual",
            "next_steps": "Add dataset manually, then call continue_setup(feature_group_id)"
        }

    except Exception as e:
        print(f"❌ Error in clone_master_project: {str(e)}")
        raise

def continue_setup(feature_group_id):
    """Continue setup after manual dataset creation"""
    try:
        if 'current_project_info' not in globals():
            raise ValueError("No project info found. Run clone_master_project first.")

        info = current_project_info
        new_project_id = info["project_id"]
        new_school_name = info["school_name"]
        master_model = info["master_model"]

        print(f"Continuing setup for {new_school_name}...")

        # 4. Create model using master configuration
        print("Creating model...")
        try:
            # Get master model parameters
            master_params = getattr(master_model, 'training_config', 
                                  getattr(master_model, 'task_parameters', {}))

            # Try different model creation approaches
            new_model = None
            try:
                new_model = client.create_model(
                    project_id=new_project_id,
                    name=f"{new_school_name} Chatbot Model",
                    feature_group_ids=[feature_group_id],
                    training_config=master_params
                )
            except Exception as e1:
                print(f"Model creation attempt 1 failed: {e1}")
                try:
                    new_model = client.create_model(
                        project_id=new_project_id,
                        name=f"{new_school_name} Chatbot Model",
                        feature_group_ids=[feature_group_id]
                    )
                except Exception as e2:
                    print(f"Model creation attempt 2 failed: {e2}")
                    # Create basic model
                    new_model = client.create_model(
                        project_id=new_project_id,
                        name=f"{new_school_name} Chatbot Model"
                    )

            print(f"✅ Created model: {new_model.model_id}")

        except Exception as e:
            print(f"❌ Model creation failed: {e}")
            return {"error": "Model creation failed", "details": str(e)}

        # 5. Train model
        print("Starting model training...")
        try:
            client.train_model(new_model.model_id)
            print(f"✅ Training started for model: {new_model.model_id}")
        except Exception as e:
            print(f"⚠️  Training start failed: {e}")

        # 6. Wait for training (optional)
        print("You can monitor training progress in the web console...")
        print(f"Model training URL: https://console.abacus.ai/models/{new_model.model_id}")

        # 7. Deploy model
        print("Attempting to deploy model...")
        deployment = None
        deployment_id = None

        try:
            deployment = client.create_deployment(
                model_id=new_model.model_id,
                name=f"{new_school_name} Deployment"
            )
            deployment_id = getattr(deployment, 'deployment_id', 
                                  getattr(deployment, 'id', None))
            print(f"✅ Created deployment: {deployment_id}")
        except Exception as e1:
            print(f"create_deployment failed: {e1}")
            try:
                deployment = client.deploy_model(
                    model_id=new_model.model_id,
                    name=f"{new_school_name} Deployment"
                )
                deployment_id = getattr(deployment, 'deployment_id', 
                                      getattr(deployment, 'id', None))
                print(f"✅ Created deployment: {deployment_id}")
            except Exception as e2:
                print(f"❌ All deployment methods failed: {e2}")
                print(f"Manual deployment: https://console.abacus.ai/models/{new_model.model_id}")

        return {
            "project_id": new_project_id,
            "model_id": new_model.model_id,
            "deployment_id": deployment_id,
            "feature_group_id": feature_group_id,
            "status": "complete" if deployment_id else "model_created_deployment_manual"
        }

    except Exception as e:
        print(f"❌ Error in continue_setup: {str(e)}")
        raise

def quick_clone_with_manual_steps(new_school_name, gdoc_url):
    """One-step function that provides manual instructions"""
    try:
        # Create project
        result = clone_master_project(new_school_name, gdoc_url)
        project_id = result["project_id"]

        print(f"\n" + "="*60)
        print(f"🎯 SETUP INSTRUCTIONS FOR {new_school_name.upper()}")
        print(f"="*60)
        print(f"1. Go to: https://console.abacus.ai/projects/{project_id}")
        print(f"2. Click 'Add Data Source'")
        print(f"3. Choose 'Google Sheets' and enter: {gdoc_url}")
        print(f"4. Name it: '{new_school_name} Knowledge Base'")
        print(f"5. After creation, copy the Feature Group ID")
        print(f"6. Run: continue_setup('your_feature_group_id')")
        print(f"="*60)

        return result

    except Exception as e:
        print(f"❌ Setup failed: {str(e)}")
        raise

# Example usage:
# result = quick_clone_with_manual_steps("Example School", "https://docs.google.com/spreadsheets/d/your-sheet-id")
# Then after manual dataset creation:
# final_result = continue_setup("your_feature_group_id_here")