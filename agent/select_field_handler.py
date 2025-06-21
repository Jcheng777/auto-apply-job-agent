"""
Handler for select/dropdown fields in job applications.
"""

from typing import List, Dict, Optional
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Common patterns for different field types
SELECT_PATTERNS = {
    "years_experience": {
        "0-1": ["0-1", "less than 1", "under 1", "0 to 1", "0-1 years", "less than 1 year"],
        "1-3": ["1-3", "1 to 3", "1+", "1 plus", "1-3 years", "1 to 3 years"],
        "3-5": ["3-5", "3 to 5", "3+", "3 plus", "3-5 years", "3 to 5 years"],
        "5-10": ["5-10", "5 to 10", "5+", "5 plus", "5-10 years", "5 to 10 years"],
        "10+": ["10+", "10 plus", "more than 10", "over 10", "10+ years", "more than 10 years"]
    },
    "work_authorization": {
        "yes": ["yes", "authorized", "have authorization", "work permit", "i am authorized", "authorized to work"],
        "no": ["no", "need sponsorship", "require visa", "not authorized", "need work permit", "require authorization"]
    },
    "employment_type": {
        "full-time": ["full-time", "full time", "permanent", "regular"],
        "part-time": ["part-time", "part time", "temporary", "contract"],
        "contract": ["contract", "contractor", "freelance", "consultant"],
        "internship": ["internship", "intern", "co-op", "coop"]
    },
    "education_level": {
        "high_school": ["high school", "secondary", "secondary school"],
        "associate": ["associate", "associate's", "associates", "2 year degree"],
        "bachelor": ["bachelor", "bachelor's", "bachelors", "4 year degree", "undergraduate"],
        "master": ["master", "master's", "masters", "graduate"],
        "phd": ["phd", "doctorate", "doctoral", "doctor of philosophy"]
    }
}

class SelectFieldHandler:
    def __init__(self):
        # Initialize OpenAI if API key is available
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            openai.api_key = self.openai_api_key

    def get_select_options(self, element) -> List[Dict[str, str]]:
        """Get all options from a select element."""
        return element.evaluate("""e => {
            return Array.from(e.options).map(opt => ({
                text: opt.text,
                value: opt.value
            }));
        }""")

    def match_select_option(self, options: List[Dict[str, str]], user_value: str, field_type: str) -> Optional[str]:
        """
        Match user value to select options using patterns and LLM.
        
        Args:
            options: List of option dictionaries with 'text' and 'value' keys
            user_value: The value from user profile
            field_type: Type of field (e.g., 'years_experience', 'work_authorization')
            
        Returns:
            Matched option text or None if no match found
        """
        # Try pattern matching first
        if field_type in SELECT_PATTERNS:
            for key, variations in SELECT_PATTERNS[field_type].items():
                if any(variation in user_value.lower() for variation in variations):
                    # Find the closest match in options
                    for option in options:
                        if key in option['text'].lower():
                            return option['text']

        # If no pattern match and OpenAI is available, use LLM
        if self.openai_api_key:
            return self._use_llm_for_matching(options, user_value)
        
        # If no LLM available, try direct matching
        for option in options:
            if user_value.lower() in option['text'].lower():
                return option['text']
        
        return None

    def _use_llm_for_matching(self, options: List[Dict[str, str]], user_value: str) -> Optional[str]:
        """Use OpenAI to find the best matching option."""
        try:
            prompt = f"""
            Given these dropdown options:
            {[opt['text'] for opt in options]}
            
            And the user's value:
            {user_value}
            
            Which option best matches the user's value? Return only the exact option text.
            If no good match exists, return 'NO_MATCH'.
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that matches user input to dropdown options."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=50
            )

            matched_text = response.choices[0].message.content.strip()
            
            # Verify the matched text exists in options
            if matched_text != 'NO_MATCH' and any(opt['text'] == matched_text for opt in options):
                return matched_text
            
            return None

        except Exception as e:
            print(f"Error using LLM for matching: {str(e)}")
            return None

    def determine_field_type(self, label: str, name: str, placeholder: str) -> str:
        """Determine the type of select field based on its attributes."""
        combined_text = f"{label} {name} {placeholder}".lower()
        
        if any(word in combined_text for word in ["experience", "years", "year"]):
            return "years_experience"
        if any(word in combined_text for word in ["authorized", "authorization", "work permit", "visa", "sponsorship"]):
            return "work_authorization"
        if any(word in combined_text for word in ["employment", "job type", "position type"]):
            return "employment_type"
        if any(word in combined_text for word in ["education", "degree", "qualification"]):
            return "education_level"
            
        return "text"  # default type 