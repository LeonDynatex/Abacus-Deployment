import abacusai
import os
from dotenv import load_dotenv

load_dotenv()
client = abacusai.ApiClient(api_key=os.getenv("ABACUS_API_KEY"))
MASTER_PROJECT_ID = os.getenv("MASTER_PROJECT_ID")

def setup_new_school_project(new_school_name):
    """
    Step 1: Create project and provide manual setup instructions
    """
    try:
        # Create new project
        print(f"Creating project for {new_school_name}...")
        new_project = client.create_project(
            name=f"{new_school_name} Chatbot",
            use_case="CHAT_LLM"
        )
        new_project_id = new_project.project_id
        print(f"✅ Created project: {new_project_id}")

        # Get master project configuration for reference
        print("Getting master project configuration...")
        master_models = client.list_models(project_id=MASTER_PROJECT_ID)
        if not master_models:
            raise ValueError("No models found in master project")

        master_model = master_models[0]
        print(f"✅ Found master model reference: {master_model.model_id}")

        # Print complete setup instructions
        print_setup_instructions(new_school_name, new_project_id)

        return {
            "project_id": new_project_id,
            "school_name": new_school_name,
            "status": "project_created",
            "next_step": "complete_manual_steps"
        }

    except Exception as e:
        print(f"❌ Error in setup_new_school_project: {str(e)}")
        raise

def create_document_retriever(project_id, school_name, feature_group_id):
    """
    Step 2: Create document retriever after manual dataset setup
    """
    try:
        retriever = client.create_document_retriever(
            name=f"{school_name}_Document_Retriever",
            project_id=project_id,
            feature_group_id=feature_group_id
        )
        print(f"✅ Created document retriever: {retriever.document_retriever_id}")
        
        # Print next manual steps
        print_training_instructions(school_name, project_id, retriever.document_retriever_id)
        
        return {
            "retriever_id": retriever.document_retriever_id,
            "project_id": project_id,
            "school_name": school_name,
            "status": "retriever_created",
            "next_step": "manual_training_and_deployment"
        }
    except Exception as e:
        print(f"❌ Error creating document retriever: {str(e)}")
        raise

def print_setup_instructions(school_name, project_id):
    """Print formatted setup instructions"""
    print(f"\n" + "="*70)
    print(f"🎯 SETUP INSTRUCTIONS FOR {school_name.upper()}")
    print(f"="*70)
    print(f"📋 STEP 1: ADD DATA SOURCE")
    print(f"   1. Go to: https://console.abacus.ai/projects/{project_id}")
    print(f"   2. Click 'Add Data Source'")
    print(f"   3. Choose 'Google Sheets'")
    print(f"   4. Name it: '{school_name} Knowledge Base'")
    print(f"   5. Click 'Create Feature Group'")
    print(f"   6. ✅ Check here when completed: [ ]")
    print(f"\n📋 AFTER STEP 1 IS COMPLETE:")
    print(f"   7. Copy the Feature Group ID from the created feature group")
    print(f"   8. Run: create_document_retriever('{project_id}', '{school_name}', 'YOUR_FEATURE_GROUP_ID')")
    print(f"="*70)

def print_training_instructions(school_name, project_id, retriever_id):
    """Print training and deployment instructions"""
    print(f"\n" + "="*70)
    print(f"🎯 TRAINING & DEPLOYMENT FOR {school_name.upper()}")
    print(f"="*70)
    print(f"📋 STEP 2: CREATE AND TRAIN MODEL (MANUAL)")
    print(f"   1. Go to: https://console.abacus.ai/projects/{project_id}")
    print(f"   2. Click 'Create Model'")
    print(f"   3. Select 'Chat LLM' use case")
    print(f"   4. Name: '{school_name}_Chatbot_Model'")
    print(f"   5. Select your document retriever: {retriever_id}")
    print(f"   6. Click 'Create Model'")
    print(f"   7. Click 'Train Model'")
    print(f"   8. Wait for training to complete")
    print(f"   9. ✅ Check here when training is complete: [ ]")
    print(f"\n📋 STEP 3: CREATE DEPLOYMENT (MANUAL)")
    print(f"   10. After training completes, click 'Deploy Model'")
    print(f"   11. Name: '{school_name}_Deployment'")
    print(f"   12. Configure deployment settings as needed")
    print(f"   13. Click 'Create Deployment'")
    print(f"   14. ✅ Check here when deployment is live: [ ]")
    print(f"\n🎉 SETUP COMPLETE!")
    print(f"   Your {school_name} chatbot should now be ready to use!")
    print(f"="*70)

def quick_setup_with_checklist(new_school_name):
    """
    Complete setup function with manual checklist approach
    """
    try:
        print(f"🚀 Starting setup for {new_school_name}...")
        result = setup_new_school_project(new_school_name)
        
        print(f"\n📝 SETUP SUMMARY:")
        print(f"   • Project ID: {result['project_id']}")
        print(f"   • School Name: {result['school_name']}")
        print(f"   • Status: {result['status']}")
        print(f"\n💡 NEXT: Follow the manual steps above, then run create_document_retriever()")
        
        return result

    except Exception as e:
        print(f"❌ Setup failed: {str(e)}")
        raise

def print_checklist_summary():
    """Print a summary checklist for tracking progress"""
    print(f"\n" + "="*50)
    print(f"📋 SETUP PROGRESS CHECKLIST")
    print(f"="*50)
    print(f"[ ] Step 1: Run quick_setup_with_checklist()")
    print(f"[ ] Step 2: Add data source in Abacus console")
    print(f"[ ] Step 3: Run create_document_retriever()")
    print(f"[ ] Step 4: Create & train model in Abacus console")
    print(f"[ ] Step 5: Deploy model in Abacus console")
    print(f"[ ] Step 6: Test chatbot")
    print(f"="*50)

# Example usage:
# print_checklist_summary()
# result = quick_setup_with_checklist("Example School", "https://docs.google.com/spreadsheets/d/your-sheet-id")
# 
# After completing manual Step 1 in Abacus console:
# create_document_retriever("project_id", "school_name", "feature_group_id")
#
# Then complete Steps 2-3 manually in Abacus console following the printed instructions 