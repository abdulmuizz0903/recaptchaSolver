"""
Legacy reCAPTCHA solver using the original approach.
This file is now refactored to use the new generalized RecaptchaSolver class.

This demonstrates how to migrate from the old approach to the new one.
"""

import os
import time
from recaptcha_solver import RecaptchaSolver, setup_edge_with_buster

# --- 1. CONFIGURATION ---
RELATIVE_CRX_PATH = "extensions/buster.crx"
URL = "https://patrickhlauke.github.io/recaptcha/"

# --- VALIDATE CRX FILE PATH ---
CRX_FILE_PATH = os.path.abspath(RELATIVE_CRX_PATH)
if not os.path.exists(CRX_FILE_PATH):
    print(f"Error: The CRX file was not found at '{CRX_FILE_PATH}'")
    exit()

# --- 2. SETUP EDGE OPTIONS AND DRIVER (New simplified approach) ---
print("Setting up Edge with Buster extension...")
driver = setup_edge_with_buster(CRX_FILE_PATH)

print("Edge started with Buster extension installed.")

try:
    # --- 3. CREATE SOLVER AND SOLVE RECAPTCHA (New simplified approach) ---
    print(f"Navigating to {URL}...")
    driver.get(URL)
    
    # Add a small delay for the page to load fully
    time.sleep(1)
    
    # Create the solver instance with debug enabled
    solver = RecaptchaSolver(driver, debug=True)
    
    # Solve the reCAPTCHA using the new generalized method
    print("Attempting to solve reCAPTCHA using the generalized solver...")
    success = solver.solve_recaptcha(max_wait_time=30)
    
    if success:
        print("✅ reCAPTCHA solved successfully!")
    else:
        print("❌ Failed to solve reCAPTCHA")

finally:
    # --- 4. CLEANUP ---
    print("Script finished. Closing browser in 10 seconds...")
    time.sleep(10)
    driver.quit()