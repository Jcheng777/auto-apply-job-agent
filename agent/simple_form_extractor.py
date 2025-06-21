from playwright.sync_api import sync_playwright

IMPORTANT_KEYWORDS = [
    # Personal Information
    "name", "email", "phone", "linkedin", "address", "resume", "cv",
    # Work Authorization
    "authorized", "authorization", "work permit", "visa", "sponsorship",
    "citizenship", "citizen", "permanent resident", "green card", "countries", "states"
    # Common Questions
    "experience", "years", "salary", "expected salary", "desired salary",
    "notice period", "available", "start date", "relocation", "remote",
    "hybrid", "onsite", "work location", "job location",
    # File Uploads
    "upload", "attach", "file", "document", "pdf", "doc", "docx",
    # Extra Fields
    "github", "twitter", "X", "github", "website", "linkedin",
    # Acknowledgement
    "acknowledge", "accept", "confirm", "agree", "acceptance", "acknowledgment",
    "acknowledgement", "acceptance", "confirmation", "acceptance", "acknowledgment",
    "acknowledgement", "acceptance", "confirmation", "acceptance", "acknowledgment", "accuracy"

    #U.S. Standard Demographic Questions
    # gender
    "gender", "identity", "describe", "transgender", "sexual", "sexual orientation"

    # race
    "racial", "race", "ethnic",

    # disability
    "disability", "crhonic", "chronic condition"

    # veteran status
    "veteran", "veteran status", "active member"

    # Commute
    "commute", "commuting", "located"

]

def extract_important_fields(url):
    important_fields = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # See browser action during testing
        page = browser.new_page()
        page.goto(url, timeout=60000)  # 60 sec timeout

        # Grab all input, textarea, and select fields
        form_elements = page.query_selector_all("input, textarea, select")

        for element in form_elements:
            tag = element.evaluate("e => e.tagName").lower()
            element_type = element.get_attribute("type") or tag
            id_attr = element.get_attribute("id")
            name_attr = element.get_attribute("name")
            placeholder = element.get_attribute("placeholder") or ""
            class_attr = element.get_attribute("class") or ""
            # Try to find label (either linked by "for" attribute or closest label)
            label = ""
            try:
                if id_attr:
                    label_element = page.query_selector(f"label[for='{id_attr}']")
                    if label_element:
                        label = label_element.inner_text().strip()
                if not label:
                    parent_label = element.evaluate_handle("el => el.closest('label')")
                    if parent_label:
                        label = parent_label.evaluate("e => e.innerText").strip()
            except Exception:
                pass

            # Get the field's value if it exists
            value = ""
            try:
                if element_type == "select":
                    value = element.evaluate("e => e.value")
                else:
                    value = element.get_attribute("value") or ""
            except Exception:
                pass

            field_info = {
                "label": label,
                "type": element_type,
                "id": id_attr,
                "name": name_attr,
                "placeholder": placeholder,
                "value": value,
                "class": class_attr,
                "is_required": element.get_attribute("required") is not None,
                "field_type": determine_field_type(label, name_attr, placeholder, element_type, class_attr)
            }

            # Check if label, name, or placeholder matches important fields
            combined_text = (f"{label} {name_attr} {placeholder}").lower()
            if any(keyword in combined_text for keyword in IMPORTANT_KEYWORDS):
                important_fields.append(field_info)

        browser.close()

    return important_fields

def determine_field_type(label, name, placeholder, element_type, class_attr):
    """Determine the semantic type of the field based on its attributes."""
    combined_text = f"{label} {name} {placeholder} {class_attr}".lower()
    
    # Check for select__input class pattern
    if "select__input" in combined_text:
        return "select-one"
    
    # Select fields
    if element_type == "select-one":
        return "select-one"  # Generic select field
    
    # File upload fields
    if element_type == "file" or "upload" in combined_text or "attach" in combined_text:
        return "file_upload"
    
    # Work authorization fields
    if any(word in combined_text for word in ["authorized", "authorization", "work permit", "visa", "sponsorship"]):
        return "work_authorization"
    
    # Yes/No questions
    if element_type == "radio" or element_type == "checkbox":
        return "yes_no"
    
    # Common field types
    if "name" in combined_text:
        return "name"
    if "email" in combined_text:
        return "email"
    if "phone" in combined_text or "telephone" in combined_text:
        return "phone"
    if "linkedin" in combined_text:
        return "linkedin"
    if "address" in combined_text:
        return "address"
    if "resume" in combined_text or "cv" in combined_text:
        return "resume"
    if "salary" in combined_text:
        return "salary"
    if "experience" in combined_text:
        return "experience"
    
    return "text"  # default type

if __name__ == "__main__":
    # Example usage with a test URL
    test_url = "https://www.linkedin.com/jobs/application/0/"  # Replace with an actual job application URL
    results = extract_important_fields(test_url)
    print("\nImportant fields found:")
    for field in results:
        print(f"\nField: {field}")
