"""
User profile information for autofilling job applications.
"""

class UserProfile:
    def __init__(self):
        # Basic information
        self.name = ""
        self.email = ""
        self.phone = ""
        self.linkedin = ""
        self.address = ""
        self.resume_path = ""
        
        # Additional information
        self.website = ""
        self.github = ""
        self.portfolio = ""
        self.summary = ""
        
        # Work experience
        self.current_company = ""
        self.current_position = ""
        self.years_experience = 0
        
        # Education
        self.education = []
        self.skills = []
        
        # Work Authorization
        self.work_authorized = True  # Default to True, update as needed
        self.requires_sponsorship = False  # Default to False, update as needed
        self.citizenship = "US Citizen"  # e.g., "US Citizen", "Permanent Resident"
        self.visa_status = ""  # e.g., "H1B", "Green Card"
        
        # Job Preferences
        self.desired_salary = "100000"
        self.notice_period = "2 weeks"  # Default notice period
        self.available_start_date = ""  # Leave empty for immediate
        self.willing_to_relocate = True
        self.preferred_work_location = ""  # e.g., "Remote", "San Francisco, CA"
        
    def load_from_file(self, file_path):
        """Load user profile from a JSON file."""
        import json
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                for key, value in data.items():
                    if hasattr(self, key):
                        setattr(self, key, value)
            return True
        except Exception as e:
            print(f"Error loading profile: {e}")
            return False
            
    def save_to_file(self, file_path):
        """Save user profile to a JSON file."""
        import json
        try:
            data = {attr: getattr(self, attr) for attr in dir(self) 
                   if not attr.startswith('_') and not callable(getattr(self, attr))}
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving profile: {e}")
            return False
            
    def get_value_for_field(self, field_info):
        """Get the appropriate value for a form field based on its information."""
        # Debug: Print all arguments and their types
        import inspect
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        print("\nDEBUG - get_value_for_field arguments:")
        for arg in args:
            print(f"  {arg}: {values[arg]}")
        
        field_type = field_info.get('field_type', '')
        field_label = field_info.get('label', '').lower() if field_info.get('label') else ""
        field_name = field_info.get('name', '').lower() if field_info.get('name') else ""
        field_id = field_info.get('id', '').lower() if field_info.get('id') else ""
        options = field_info.get('options', [])
        
        # Debug: Print field info
        print("\nDEBUG - Field info:")
        print(f"  field_type: {field_type}")
        print(f"  field_label: {field_label}")
        print(f"  field_name: {field_name}")
        print(f"  field_id: {field_id}")
        print(f"  options: {options}")
        
        # Handle file uploads
        if field_type == 'file_upload':
            if 'resume' in field_label or 'cv' in field_label or field_id == 'resume':
                return self.resume_path
            return None  # Don't know what file to upload for other types
            
        # Handle work authorization questions
        if field_type == 'work_authorization':
            if 'authorized' in field_label or 'authorization' in field_label:
                return self._get_yes_no_value(self.work_authorized, options)
            if 'sponsorship' in field_label:
                return self._get_yes_no_value(self.requires_sponsorship, options)
            if 'citizenship' in field_label:
                return self.citizenship
            if 'visa' in field_label:
                return self.visa_status
                
        # Handle yes/no questions
        if field_type == 'yes_no':
            if 'relocate' in field_label:
                return self._get_yes_no_value(self.willing_to_relocate, options)
            if 'remote' in field_label:
                return self._get_yes_no_value('remote' in self.preferred_work_location.lower(), options)
                
        # Handle common field types
        if field_type == 'name':
            return self.name
        if field_type == 'email':
            return self.email
        if field_type == 'phone':
            return self.phone
        if field_type == 'linkedin':
            return self.linkedin
        if field_type == 'address':
            return self.address
        if field_type == 'salary':
            return self.desired_salary
        if field_type == 'experience':
            return str(self.years_experience)
            
        # Fallback to label-based matching for other fields
        combined_text = f"{field_label} {field_name} {field_id}".lower()
        
        if any(term in combined_text for term in ["name", "full name", "fullname"]):
            return self.name
        if any(term in combined_text for term in ["email", "e-mail"]):
            return self.email
        if any(term in combined_text for term in ["phone", "telephone", "mobile", "cell"]):
            return self.phone
        if any(term in combined_text for term in ["linkedin", "linked-in", "linked in"]):
            return self.linkedin
        if any(term in combined_text for term in ["address", "location"]):
            return self.address
        if any(term in combined_text for term in ["website", "web site", "personal site"]):
            return self.website
        if any(term in combined_text for term in ["github", "git hub"]):
            return self.github
        if any(term in combined_text for term in ["portfolio"]):
            return self.portfolio
        if any(term in combined_text for term in ["summary", "about", "bio"]):
            return self.summary
        if any(term in combined_text for term in ["salary", "compensation", "pay"]):
            return self.desired_salary
        if any(term in combined_text for term in ["notice", "notice period"]):
            return self.notice_period
        if any(term in combined_text for term in ["start date", "available"]):
            return self.available_start_date
            
        return None  # No matching field found
        
    def _get_yes_no_value(self, boolean_value, options=None):
        """Helper method to get the appropriate Yes/No value based on the field's options."""
        if not options:
            return "Yes" if boolean_value else "No"
            
        # Find the matching option based on the boolean value
        for option in options:
            option_text = option["text"].lower()
            if boolean_value and option_text in ["yes", "y", "true"]:
                return option["value"]
            if not boolean_value and option_text in ["no", "n", "false"]:
                return option["value"]
                
        # Fallback to default Yes/No if no matching option found
        return "Yes" if boolean_value else "No" 