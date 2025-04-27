"""
Main script for the job application autofiller.
"""

import os
import json
from simple_form_extractor import extract_important_fields
from user_profile import UserProfile
from form_autofiller import FormAutofiller

def create_sample_profile():
    """Create a sample user profile for testing."""
    profile = UserProfile()
    
    # Basic information
    profile.name = "John Doe"
    profile.email = "john.doe@example.com"
    profile.phone = "(555) 123-4567"
    profile.linkedin = "https://linkedin.com/in/johndoe"
    profile.address = "123 Main St, Anytown, USA"
    profile.resume_path = os.path.join(os.path.dirname(__file__), "sample_resume.pdf")
    
    # Additional information
    profile.website = "https://johndoe.com"
    profile.github = "https://github.com/johndoe"
    profile.portfolio = "https://johndoe.com/portfolio"
    profile.summary = "Experienced software developer with a passion for automation."
    
    # Work experience
    profile.current_company = "Tech Corp"
    profile.current_position = "Senior Software Engineer"
    profile.years_experience = 5
    
    # Education and skills
    profile.education = [
        {"degree": "BS Computer Science", "school": "University of Technology", "year": 2018}
    ]
    profile.skills = ["Python", "JavaScript", "React", "Node.js", "AWS"]
    
    # Work Authorization
    profile.work_authorized = True
    profile.requires_sponsorship = False
    profile.citizenship = "US Citizen"
    profile.visa_status = "N/A"
    
    # Job Preferences
    profile.desired_salary = "150000"
    profile.notice_period = "2 weeks"
    profile.available_start_date = "Immediate"
    profile.willing_to_relocate = True
    profile.preferred_work_location = "Remote or San Francisco, CA"
    
    # Save the profile
    profile_path = os.path.join(os.path.dirname(__file__), "user_profile.json")
    profile.save_to_file(profile_path)
    return profile_path

def main():
    """Main function to run the job application autofiller."""
    print("Job Application Autofiller")
    print("=========================")
    
    # Check if user profile exists, if not create a sample one
    profile_path = os.path.join(os.path.dirname(__file__), "user_profile.json")
    if not os.path.exists(profile_path):
        print("No user profile found. Creating a sample profile for testing...")
        profile_path = create_sample_profile()
    
    # Load the user profile
    user_profile = UserProfile()
    if not user_profile.load_from_file(profile_path):
        print("Error loading user profile. Please check the file format.")
        return
    
    # Create the form autofiller
    autofiller = FormAutofiller(user_profile)
    
    try:
        # Get the job application URL
        url = input("Paste a job application page URL: ")
        
        # Ask what action to perform
        print("\nWhat would you like to do?")
        print("1. Extract form fields only")
        print("2. Fill form fields (without submitting)")
        print("3. Fill and submit form")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            # Extract form fields only
            important_fields = extract_important_fields(url)
            
            print("\n--- Important Fields Found ---")
            for field in important_fields:
                print(f"Label: {field['label']} | ID: {field['id']} | Name: {field['name']} | Type: {field['type']}")
                
        elif choice == "2":
            # Fill form fields without submitting
            result = autofiller.fill_form(url, headless=False)
            
            if "error" in result:
                print(f"\nError: {result['error']}")
            else:
                print("\n--- Filled Fields ---")
                for field in result["filled_fields"]:
                    print(f"Field: {field['field']} | Value: {field['value']} | Status: {field['status']}")
                
                print(f"\nFull-page screenshot saved as: {result['screenshot']}")
                print("\nBrowser will remain open indefinitely. Press Enter when you want to close it...")
                input()
                autofiller.close_browser()
                
        elif choice == "3":
            # Fill and submit form
            result = autofiller.submit_form(url, headless=False)
            
            if "error" in result:
                print(f"\nError: {result['error']}")
            else:
                print(f"\nForm submission status: {result['status']}")
                if "screenshot" in result:
                    print(f"Full-page screenshot saved as: {result['screenshot']}")
                print("\nBrowser will remain open indefinitely. Press Enter when you want to close it...")
                input()
                autofiller.close_browser()
        else:
            print("Invalid choice. Please run the script again.")
    finally:
        # Make sure to close the browser when the script exits
        autofiller.close_browser()

if __name__ == "__main__":
    main()
