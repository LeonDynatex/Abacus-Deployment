import abacusai
import os
from dotenv import load_dotenv

load_dotenv()
client = abacusai.ApiClient(api_key=os.getenv("ABACUS_API_KEY"))
MASTER_PROJECT_ID = os.getenv("MASTER_PROJECT_ID")


def clone_master_project(new_school_name, gdoc_url):
    try:
        # 1. Create new project
        new_project = client.create_project(name=f"{new_school_name} Chatbot",
                                            use_case="CHAT_LLM")
        new_project_id = new_project.project_id
        print(f"Created project: {new_project_id}")

        # 2. Create dataset - try different approaches
        dataset = None
        try:
            # Approach 1: Basic feature group creation
            dataset = client.create_feature_group(
                project_id=new_project_id,
                table_name=f"{new_school_name}_knowledge_base",
                source_type="GOOGLE_SHEETS",
                location=gdoc_url)
        except Exception as e1:
            print(f"Method 1 failed: {e1}")
            try:
                # Approach 2: Different parameter names
                dataset = client.create_feature_group(
                    project_id=new_project_id,
                    feature_group_name=f"{new_school_name}_knowledge_base",
                    source="GOOGLE_SHEETS",
                    google_sheets_url=gdoc_url)
            except Exception as e2:
                print(f"Method 2 failed: {e2}")
                try:
                    # Approach 3: Minimal parameters
                    dataset = client.create_feature_group(
                        project_id=new_project_id, location=gdoc_url)
                except Exception as e3:
                    print(f"Method 3 failed: {e3}")
                    raise Exception("Could not create dataset with any method")

        if dataset:
            dataset_id = getattr(dataset, 'feature_group_id',
                                 getattr(dataset, 'dataset_id', None))
            print(f"Created dataset: {dataset_id}")
        else:
            raise Exception("Dataset creation failed")

        # 3. Get master model parameters
        master_models = client.list_models(project_id=MASTER_PROJECT_ID)
        if not master_models:
            raise ValueError("No models found in master project")

        master_model = master_models[0]
        master_params = getattr(master_model, 'task_parameters', {})
        print(f"Retrieved master model: {master_model.model_id}")

        # 4. Create model - try different approaches
        new_model = None
        try:
            # Approach 1: With feature_group_ids
            new_model = client.create_model(
                project_id=new_project_id,
                name=f"{new_school_name} Chatbot Model",
                use_case="LLM_AGENT",
                feature_group_ids=[dataset_id],
                training_config=master_params)
        except Exception as e1:
            print(f"Model creation method 1 failed: {e1}")
            try:
                # Approach 2: With dataset_ids
                new_model = client.create_model(
                    project_id=new_project_id,
                    name=f"{new_school_name} Chatbot Model",
                    dataset_ids=[dataset_id],
                    training_config=master_params)
            except Exception as e2:
                print(f"Model creation method 2 failed: {e2}")
                # Approach 3: Minimal model creation
                new_model = client.create_model(
                    project_id=new_project_id,
                    name=f"{new_school_name} Chatbot Model")

        print(f"Created model: {new_model.model_id}")

        # 5. Train model
        try:
            client.train_model(new_model.model_id)
            print(f"Training started for model: {new_model.model_id}")
        except Exception as e:
            print(f"Training failed: {e}")

        # 6. Deploy model
        deployment = None
        try:
            deployment = client.create_deployment(
                model_id=new_model.model_id,
                name=f"{new_school_name} Deployment")
        except Exception as e1:
            print(f"Deployment method 1 failed: {e1}")
            try:
                deployment = client.deploy_model(
                    model_id=new_model.model_id,
                    name=f"{new_school_name} Deployment")
            except Exception as e2:
                print(f"Deployment method 2 failed: {e2}")
                deployment = None

        if deployment:
            print(f"Created deployment: {deployment.deployment_id}")

        return {
            "project_id":
            new_project_id,
            "model_id":
            new_model.model_id,
            "deployment_id":
            getattr(deployment, 'deployment_id', None) if deployment else None,
            "dataset_id":
            dataset_id
        }

    except Exception as e:
        print(f"Error in clone_master_project: {str(e)}")
        raise


# Example usage:
# result = clone_master_project("Example School", "https://docs.google.com/spreadsheets/d/your-sheet-id")
# print(result)
