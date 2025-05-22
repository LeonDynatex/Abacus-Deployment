import abacusai
import os
from dotenv import load_dotenv

load_dotenv()
client = abacusai.ApiClient(api_key=os.getenv("ABACUS_API_KEY"))
MASTER_PROJECT_ID = os.getenv("MASTER_PROJECT_ID")


def clone_master_project(new_school_name, gdoc_url):
                                # 1. Create new project
                                new_project = client.create_project(
                                    name=f"{new_school_name} Chatbot",
                                    use_case="CHAT_LLM")
                                new_project_id = new_project.project_id

                                # 2. Create dataset
                                dataset = client.create_connector_dataset(
                                    name=f"{new_school_name} Knowledge Base",
                                    project_id=new_project_id,
                                    connector_type="GOOGLE_SHEETS",
                                    data_connection_config={"url": gdoc_url})

                                # 3. Get master model parameters
                                master_model = client.list_models(
                                    project_id=MASTER_PROJECT_ID)[0]
                                master_params = master_model.task_parameters

                                # 4. Create model
                                new_model = client.create_model(
                                    project_id=new_project_id,
                                    name=f"{new_school_name} Chatbot Model",
                                    use_case="LLM_AGENT",
                                    task_type=master_model.task_type,
                                    dataset_id=dataset.dataset_id,
                                    task_parameters=master_params)

                                client.train_model(new_model.model_id)

                                # 5. Deploy model
                                deployment = client.deploy_model(
                                    model_id=new_model.model_id,
                                    name=f"{new_school_name} Deployment")

                                return {
                                    "project_id": new_project_id,
                                    "deployment_id": deployment.deployment_id
                                }