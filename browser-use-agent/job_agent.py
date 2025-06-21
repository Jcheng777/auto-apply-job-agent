from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
from user_persona import user_persona
from upload_resume import controller
import os

load_dotenv()

import asyncio

llm = ChatOpenAI(model="gpt-4o")

def build_task(user_persona):
    return (
        f"Go to https://job-boards.greenhouse.io/biltrewards/jobs/5561847004?gh_src=534d41e54us and fill out the job application form handling text inputs, textareas, selects and file uploads using user persona information. If there are questions that are not relavent to the user persona, skip them. "
        f"IMPORTANT: For file uploads, use the upload_file function with the resume path, do not just click on upload elements. "
        f"User Persona Info:\n"
        f"Name: {user_persona.name}\n"
        f"Email: {user_persona.email}\n"
        f"Phone: {user_persona.phone}\n"
        f"LinkedIn: {user_persona.linkedin}\n"
        f"Resume Path: {user_persona.resume_path}\n"
        f"Website: {user_persona.website}\n"
        f"Github: {user_persona.github}\n"
        f"Portfolio: {user_persona.portfolio}\n"
        f"Summary: {user_persona.summary}\n"
        f"Current Company: {user_persona.current_company}\n"
        f"Current Position: {user_persona.current_position}\n"
        f"Years of Experience: {user_persona.years_experience}\n"
    )

async def main():
    # Debug: Check if resume file exists
    print(f"DEBUG: Resume path from user_persona: {user_persona.resume_path}")
    print(f"DEBUG: Current working directory: {os.getcwd()}")
    
    # Check if file exists
    if os.path.exists(user_persona.resume_path):
        print(f"DEBUG: ✅ Resume file EXISTS at: {user_persona.resume_path}")
        print(f"DEBUG: File size: {os.path.getsize(user_persona.resume_path)} bytes")
        print(f"DEBUG: File is readable: {os.access(user_persona.resume_path, os.R_OK)}")
    else:
        print(f"DEBUG: ❌ Resume file DOES NOT EXIST at: {user_persona.resume_path}")
        
        # Try to find the file in the current directory
        filename = os.path.basename(user_persona.resume_path)
        current_dir_path = os.path.join(os.getcwd(), filename)
        print(f"DEBUG: Checking if file exists in current directory: {current_dir_path}")
        if os.path.exists(current_dir_path):
            print(f"DEBUG: ✅ Found file in current directory: {current_dir_path}")
            user_persona.resume_path = current_dir_path
        else:
            print(f"DEBUG: ❌ File not found in current directory either")
            
            # List files in current directory to help debug
            print(f"DEBUG: Files in current directory:")
            try:
                for file in os.listdir(os.getcwd()):
                    if file.lower().endswith('.pdf'):
                        print(f"  - {file}")
            except Exception as e:
                print(f"DEBUG: Error listing directory: {e}")

    task = build_task(user_persona)

    available_file_paths = [user_persona.resume_path]
    print(f"DEBUG: Available file paths for agent: {available_file_paths}")
    
    # Debug: Check if upload controller is properly configured
    print(f"DEBUG: Upload controller type: {type(controller)}")
    print(f"DEBUG: Upload controller has upload_file function: {hasattr(controller, 'upload_file')}")
    
    # Debug: Check if the resume path is in available_file_paths
    print(f"DEBUG: Resume path in available_file_paths: {user_persona.resume_path in available_file_paths}")

    agent = Agent(
        task=task,
        llm=llm,
        controller=controller,
        available_file_paths=available_file_paths,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())