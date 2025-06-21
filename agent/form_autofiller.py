"""
Form autofiller for job applications using Playwright.
"""

from playwright.sync_api import sync_playwright
from simple_form_extractor import extract_important_fields
from user_profile import UserProfile
from select_field_handler import SelectFieldHandler
import time
import os

class FormAutofiller:
    def __init__(self, user_profile):
        """
        Initialize the form autofiller with a user profile.
        
        Args:
            user_profile (UserProfile): The user profile containing information to fill forms with.
        """
        self.user_profile = user_profile
        self.playwright = None
        self.browser = None
        self.page = None
        self.select_handler = SelectFieldHandler()
        
    def start_browser(self, headless=False):
        """Start the browser if it's not already running."""
        if not self.browser:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=headless)
            self.page = self.browser.new_page()
            self.page.set_default_timeout(30000)  # 30 seconds
            
    def close_browser(self):
        """Close the browser and cleanup resources."""
        if self.browser:
            self.browser.close()
            self.browser = None
        if self.playwright:
            self.playwright.stop()
            self.playwright = None
        self.page = None
        
    def take_full_page_screenshot(self, path):
        """Take a screenshot of the entire page, not just the visible viewport."""
        # Save the current viewport size
        original_viewport = self.page.viewport_size
        
        # Scroll to the top of the page
        self.page.evaluate("window.scrollTo(0, 0)")
        time.sleep(1)  # Wait for any animations to complete
        
        # Take the screenshot with full_page=True
        self.page.screenshot(path=path, full_page=True)
        
        # Restore the original viewport size
        if original_viewport:
            self.page.set_viewport_size(original_viewport)
        
    def fill_form(self, url, headless=False, slow_mo=100):
        """
        Fill a job application form with user information.
        
        Args:
            url (str): The URL of the job application form.
            headless (bool): Whether to run the browser in headless mode.
            slow_mo (int): Delay between actions in milliseconds.
            
        Returns:
            dict: Information about the filled form fields.
        """
        # First extract the important fields
        important_fields = extract_important_fields(url)
        
        filled_fields = []
        
        try:
            # Start browser if not already running
            self.start_browser(headless)
            
            # Set a reasonable viewport size
            self.page.set_viewport_size({"width": 1280, "height": 800})
            
            # Navigate to the form
            self.page.goto(url, wait_until="networkidle")
            
            # Fill each important field
            for field in important_fields:
                field_id = field.get("id")
                field_name = field.get("name")
                field_type = field.get("type")
                field_label = field.get("label")
                
                # Get the value from the user profile
                value = self.user_profile.get_value_for_field(field)
                
                if not value:
                    continue
                
                # Handle different field types
                if field_type == "file" and field_id == "resume":
                    # Handle file uploads (resume)
                    if os.path.exists(value):
                        file_input = self.page.query_selector(f"input[type='file']")
                        if file_input:
                            file_input.set_input_files(value)
                            filled_fields.append({
                                "field": field_label or field_name or field_id,
                                "value": f"File: {os.path.basename(value)}",
                                "status": "filled"
                            })
                else:
                    # Handle text inputs, textareas, and selects
                    selector = None
                    if field_id:
                        selector = f"#{field_id}"
                    elif field_name:
                        selector = f"[name='{field_name}']"
                    
                    if selector:
                        element = self.page.query_selector(selector)
                        if element:
                            # Check if it's a select element
                            if field_type == "select-one":
                                # Get all options
                                options = self.select_handler.get_select_options(element)
                                
                                # Determine field type for better matching
                                field_type = self.select_handler.determine_field_type(
                                    field_label or "",
                                    field_name or "",
                                    field.get("placeholder", "")
                                )
                                
                                # Get the best match
                                matched_value = self.select_handler.match_select_option(
                                    options,
                                    value,
                                    field_type
                                )
                                
                                if matched_value:
                                    try:
                                        # Try to select by label first
                                        element.select_option(label=matched_value)
                                        filled_fields.append({
                                            "field": field_label or field_name or field_id,
                                            "value": matched_value,
                                            "status": "filled"
                                        })
                                    except:
                                        # Fallback to value if label selection fails
                                        element.select_option(value=matched_value)
                                        filled_fields.append({
                                            "field": field_label or field_name or field_id,
                                            "value": matched_value,
                                            "status": "filled (by value)"
                                        })
                                else:
                                    filled_fields.append({
                                        "field": field_label or field_name or field_id,
                                        "value": value,
                                        "status": "failed - no matching option"
                                    })
                            else:
                                # Fill text input or textarea
                                element.fill(value)
                                filled_fields.append({
                                    "field": field_label or field_name or field_id,
                                    "value": value,
                                    "status": "filled"
                                })
            
            # Take a screenshot for verification
            screenshot_path = "form_filled.png"
            self.take_full_page_screenshot(screenshot_path)
            
            return {
                "filled_fields": filled_fields,
                "screenshot": screenshot_path
            }
            
        except Exception as e:
            return {
                "error": str(e)
            }
                
    def submit_form(self, url, submit_button_selector=None, headless=False):
        """
        Fill and submit a job application form.
        
        Args:
            url (str): The URL of the job application form.
            submit_button_selector (str): CSS selector for the submit button.
            headless (bool): Whether to run the browser in headless mode.
            
        Returns:
            dict: Information about the form submission.
        """
        # First fill the form
        result = self.fill_form(url, headless=headless)
        
        if "error" in result:
            return result
            
        try:
            # Navigate to the form
            self.page.goto(url, wait_until="networkidle")
            
            # Fill the form again (since we're in a new browser session)
            for field in result["filled_fields"]:
                field_name = field["field"]
                value = field["value"]
                
                # Find and fill the field
                element = self.page.query_selector(f"[name='{field_name}']")
                if element:
                    element.fill(value)
            
            # Find and click the submit button
            if submit_button_selector:
                submit_button = self.page.query_selector(submit_button_selector)
            else:
                # Try common submit button selectors
                submit_button = (
                    self.page.query_selector("button[type='submit']") or
                    self.page.query_selector("input[type='submit']") or
                    self.page.query_selector("button:has-text('Submit')") or
                    self.page.query_selector("button:has-text('Apply')")
                )
            
            if submit_button:
                submit_button.click()
                
                # Wait for navigation or form submission
                self.page.wait_for_load_state("networkidle")
                
                # Take a screenshot of the result
                screenshot_path = "form_submitted.png"
                self.take_full_page_screenshot(screenshot_path)
                
                return {
                    "status": "submitted",
                    "screenshot": screenshot_path
                }
            else:
                return {
                    "error": "Submit button not found"
                }
                
        except Exception as e:
            return {
                "error": str(e)
            } 