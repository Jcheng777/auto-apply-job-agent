from pydantic import BaseModel

class UserPersona(BaseModel):
    name: str
    email: str
    phone: str
    linkedin: str
    resume_path: str
    website: str
    github: str
    portfolio: str
    summary: str
    current_company: str
    current_position: str
    years_experience: int
    # Add more fields as needed

user_persona = UserPersona(
    name="Jane Doe",
    email="jane@example.com",
    phone="123-456-7890",
    linkedin="https://linkedin.com/in/janedoe",
    resume_path="/Users/jessecheng/auto-apply-job-agent/browser-use-agent/Fake Resume.pdf",
    website="https://jane.com",
    github="https://github.com/janedoe",
    portfolio="https://jane.com/portfolio",
    summary="Jane is a software engineer with 10 years of experience in the industry.",
    current_company="Google",
    current_position="Software Engineer",
    years_experience=10
) 