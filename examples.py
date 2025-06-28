"""
Example usage of the RecaptchaSolver class

This file demonstrates how to use the generalized reCAPTCHA solver
with different websites and scenarios.
"""

import os
import time
from recaptcha_solver import RecaptchaSolver, setup_edge_with_buster, setup_chrome_with_buster


def example_basic_usage():
    """Basic example: Solve reCAPTCHA on a test page"""
    
    # Configuration
    EXTENSION_PATH = os.path.abspath("extensions/buster.crx")
    TEST_URL = "https://patrickhlauke.github.io/recaptcha/"
    
    # Validate extension exists
    if not os.path.exists(EXTENSION_PATH):
        print(f"Error: Buster extension not found at '{EXTENSION_PATH}'")
        return
    
    # Setup browser with Buster extension
    print("Setting up browser with Buster extension...")
    driver = setup_edge_with_buster(EXTENSION_PATH)
    
    try:
        # Create solver instance
        solver = RecaptchaSolver(driver, debug=True)
        
        # Navigate to test page
        print(f"Navigating to {TEST_URL}...")
        driver.get(TEST_URL)
        
        # Solve the reCAPTCHA
        print("Attempting to solve reCAPTCHA...")
        success = solver.solve_recaptcha()
        
        if success:
            print("✅ Success! reCAPTCHA solved successfully!")
        else:
            print("❌ Failed to solve reCAPTCHA")
            
        # Keep browser open for a moment to see the result
        print("Keeping browser open for 10 seconds...")
        time.sleep(10)
        
    finally:
        driver.quit()


def example_multiple_attempts():
    """Example: Try multiple attempts if first one fails"""
    
    EXTENSION_PATH = os.path.abspath("extensions/buster.crx")
    TEST_URL = "https://patrickhlauke.github.io/recaptcha/"
    
    if not os.path.exists(EXTENSION_PATH):
        print(f"Error: Buster extension not found at '{EXTENSION_PATH}'")
        return
    
    driver = setup_edge_with_buster(EXTENSION_PATH)
    
    try:
        solver = RecaptchaSolver(driver, timeout=15, debug=True)
        driver.get(TEST_URL)
        
        # Use the solve_all_recaptchas method for multiple attempts
        success = solver.solve_all_recaptchas(max_attempts=3)
        
        if success:
            print("✅ reCAPTCHA solved with multiple attempts!")
        else:
            print("❌ Failed to solve reCAPTCHA after multiple attempts")
            
        time.sleep(5)
        
    finally:
        driver.quit()


def example_with_chrome():
    """Example: Using Chrome instead of Edge"""
    
    EXTENSION_PATH = os.path.abspath("extensions/buster.crx")
    TEST_URL = "https://patrickhlauke.github.io/recaptcha/"
    
    if not os.path.exists(EXTENSION_PATH):
        print(f"Error: Buster extension not found at '{EXTENSION_PATH}'")
        return
    
    # Setup Chrome with Buster extension
    print("Setting up Chrome with Buster extension...")
    driver = setup_chrome_with_buster(EXTENSION_PATH)
    
    try:
        solver = RecaptchaSolver(driver, debug=True)
        driver.get(TEST_URL)
        
        success = solver.solve_recaptcha()
        
        if success:
            print("✅ reCAPTCHA solved using Chrome!")
        else:
            print("❌ Failed to solve reCAPTCHA")
            
        time.sleep(5)
        
    finally:
        driver.quit()


def example_custom_website():
    """Example: Using the solver on a custom website"""
    
    EXTENSION_PATH = os.path.abspath("extensions/buster.crx")
    # Replace with your target website
    TARGET_URL = "https://example.com/contact"
    
    if not os.path.exists(EXTENSION_PATH):
        print(f"Error: Buster extension not found at '{EXTENSION_PATH}'")
        return
    
    driver = setup_edge_with_buster(EXTENSION_PATH)
    
    try:
        solver = RecaptchaSolver(driver, debug=True)
        
        print(f"Navigating to {TARGET_URL}...")
        driver.get(TARGET_URL)
        
        # You might need to interact with the page first
        # For example, fill out a form that triggers the reCAPTCHA
        
        # Wait for page to load
        time.sleep(3)
        
        # Solve any reCAPTCHAs on the page
        print("Looking for reCAPTCHAs to solve...")
        success = solver.solve_recaptcha()
        
        if success:
            print("✅ reCAPTCHA solved! You can now submit the form.")
            # Continue with your automation...
        else:
            print("❌ No reCAPTCHA found or failed to solve")
            
        time.sleep(10)
        
    finally:
        driver.quit()


def example_integration_with_existing_script():
    """Example: Integrating the solver into an existing automation script"""
    
    EXTENSION_PATH = os.path.abspath("extensions/buster.crx")
    
    if not os.path.exists(EXTENSION_PATH):
        print(f"Error: Buster extension not found at '{EXTENSION_PATH}'")
        return
    
    # Your existing WebDriver setup
    driver = setup_edge_with_buster(EXTENSION_PATH)
    
    try:
        # Your existing automation code
        driver.get("https://example.com/login")
        
        # Fill out login form
        # driver.find_element(By.ID, "username").send_keys("your_username")
        # driver.find_element(By.ID, "password").send_keys("your_password")
        
        # Create solver instance when you encounter a reCAPTCHA
        solver = RecaptchaSolver(driver)
        
        # Solve the reCAPTCHA
        if solver.solve_recaptcha():
            print("✅ reCAPTCHA solved! Continuing with automation...")
            
            # Continue with your automation
            # driver.find_element(By.ID, "submit").click()
            
        else:
            print("❌ Failed to solve reCAPTCHA. Manual intervention required.")
            
    finally:
        driver.quit()


if __name__ == "__main__":
    print("reCAPTCHA Solver Examples")
    print("=" * 40)
    
    # Run the basic example
    print("\n1. Running basic example...")
    example_basic_usage()
    
    # Uncomment to run other examples:
    
    # print("\n2. Running multiple attempts example...")
    # example_multiple_attempts()
    
    # print("\n3. Running Chrome example...")
    # example_with_chrome()
    
    # print("\n4. Running custom website example...")
    # example_custom_website()
    
    print("\nAll examples completed!")
