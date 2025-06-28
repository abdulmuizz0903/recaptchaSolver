"""
reCAPTCHA Solver - A generalized solution for solving reCAPTCHAs using the Buster extension

This module provides a reusable RecaptchaSolver class that can be integrated
with any Selenium WebDriver instance to automatically solve reCAPTCHAs.

Usage:
    from recaptcha_solver import RecaptchaSolver
    
    # Create your WebDriver instance
    driver = webdriver.Edge()
    
    # Create solver instance
    solver = RecaptchaSolver(driver)
    
    # Navigate to your target page
    driver.get("https://example.com")
    
    # Solve any reCAPTCHAs on the page
    success = solver.solve_recaptcha()

Author: reCAPTCHA Solver Contributors
License: MIT
"""

import time
import logging
from typing import Optional, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement


class RecaptchaSolver:
    """
    A generalized reCAPTCHA solver that works with any Selenium WebDriver instance.
    
    This class handles the common patterns of reCAPTCHA solving:
    1. Finding and clicking the reCAPTCHA checkbox
    2. Detecting if additional challenges appear
    3. Triggering the Buster extension to solve challenges
    4. Verifying successful completion
    """
    
    def __init__(self, driver: webdriver.Remote, timeout: int = 20, debug: bool = False):
        """
        Initialize the RecaptchaSolver.
        
        Args:
            driver: Selenium WebDriver instance (must have Buster extension installed)
            timeout: Maximum time to wait for elements (default: 20 seconds)
            debug: Enable debug logging (default: False)
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.timeout = timeout
        
        # Setup logging
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Common selectors for reCAPTCHA elements
        self.CHECKBOX_IFRAME_SELECTOR = "iframe[title='reCAPTCHA']"
        self.CHECKBOX_SELECTOR = "#recaptcha-anchor"
        self.CHECKBOX_CHECKED_SELECTOR = "#recaptcha-anchor[aria-checked='true']"
        
        # Challenge iframe selectors (multiple possible titles)
        self.CHALLENGE_IFRAME_SELECTORS = [
            "iframe[title='recaptcha challenge expires in two minutes']",
            "iframe[title='recaptcha challenge']",
            "iframe[src*='bframe']"
        ]
        
        # Buster extension selectors
        self.BUSTER_BUTTON_SELECTORS = [
            "div.help-button-holder",
            ".help-button-holder",
            "[class*='help-button']"
        ]

    def handle_extension_tabs(self) -> None:
        """Handle any additional tabs that the Buster extension might open."""
        if len(self.driver.window_handles) > 1:
            # Switch back to the main tab
            self.driver.switch_to.window(self.driver.window_handles[0])
            self.logger.info("Extension opened additional tabs. Switched back to main tab.")
            time.sleep(0.5)

    def find_recaptcha_checkbox_iframe(self) -> Optional[WebElement]:
        """
        Find the reCAPTCHA checkbox iframe.
        
        Returns:
            WebElement of the iframe or None if not found
        """
        try:
            self.logger.info("Looking for reCAPTCHA checkbox iframe...")
            iframe = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.CHECKBOX_IFRAME_SELECTOR))
            )
            self.logger.info("Found reCAPTCHA checkbox iframe")
            return iframe
        except TimeoutException:
            self.logger.warning("reCAPTCHA checkbox iframe not found")
            return None

    def click_recaptcha_checkbox(self) -> bool:
        """
        Click the reCAPTCHA checkbox.
        
        Returns:
            True if checkbox was clicked successfully, False otherwise
        """
        try:
            self.logger.info("Clicking reCAPTCHA checkbox...")
            checkbox = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.CHECKBOX_SELECTOR))
            )
            checkbox.click()
            self.logger.info("reCAPTCHA checkbox clicked")
            return True
        except TimeoutException:
            self.logger.error("Failed to click reCAPTCHA checkbox")
            return False

    def is_recaptcha_solved(self) -> bool:
        """
        Check if the reCAPTCHA is already solved (checkbox is checked).
        
        Returns:
            True if reCAPTCHA is solved, False otherwise
        """
        try:
            self.driver.find_element(By.CSS_SELECTOR, self.CHECKBOX_CHECKED_SELECTOR)
            self.logger.info("✅ reCAPTCHA is already solved!")
            return True
        except NoSuchElementException:
            self.logger.info("reCAPTCHA not yet solved")
            return False

    def find_challenge_iframe(self) -> Optional[WebElement]:
        """
        Find the reCAPTCHA challenge iframe using multiple possible selectors.
        
        Returns:
            WebElement of the challenge iframe or None if not found
        """
        for selector in self.CHALLENGE_IFRAME_SELECTORS:
            try:
                self.logger.info(f"Looking for challenge iframe with selector: {selector}")
                iframe = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                self.logger.info("Found reCAPTCHA challenge iframe")
                return iframe
            except TimeoutException:
                continue
        
        self.logger.warning("Challenge iframe not found with any selector")
        return None

    def activate_buster_extension(self) -> bool:
        """
        Activate the Buster extension to solve the challenge.
        
        Returns:
            True if Buster was activated successfully, False otherwise
        """
        for selector in self.BUSTER_BUTTON_SELECTORS:
            try:
                self.logger.info(f"Looking for Buster button with selector: {selector}")
                buster_button = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                
                self.logger.info("Waiting 5 seconds before clicking Buster button...")
                time.sleep(5)
                
                self.logger.info("Clicking Buster button...")
                buster_button.click()
                self.logger.info("Buster extension activated")
                return True
                
            except TimeoutException:
                continue
        
        self.logger.error("Failed to find or click Buster button")
        return False

    def wait_for_solution(self, max_wait_time: int = 30) -> bool:
        """
        Wait for the reCAPTCHA to be solved by the Buster extension.
        
        Args:
            max_wait_time: Maximum time to wait for solution (default: 30 seconds)
            
        Returns:
            True if reCAPTCHA was solved, False if timeout
        """
        self.logger.info(f"Waiting up to {max_wait_time} seconds for Buster to solve the challenge...")
        
        try:
            # Use a custom wait with longer timeout for solution
            solution_wait = WebDriverWait(self.driver, max_wait_time)
            solution_wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.CHECKBOX_CHECKED_SELECTOR))
            )
            self.logger.info("✅ reCAPTCHA solved successfully by Buster!")
            return True
        except TimeoutException:
            self.logger.error("❌ Timeout waiting for reCAPTCHA solution")
            return False

    def solve_recaptcha(self, max_wait_time: int = 30) -> bool:
        """
        Main method to solve reCAPTCHA on the current page.
        
        Args:
            max_wait_time: Maximum time to wait for Buster to solve (default: 30 seconds)
            
        Returns:
            True if reCAPTCHA was solved successfully, False otherwise
        """
        try:
            # Handle any extension tabs
            self.handle_extension_tabs()
            
            # Find the checkbox iframe
            checkbox_iframe = self.find_recaptcha_checkbox_iframe()
            if not checkbox_iframe:
                self.logger.warning("No reCAPTCHA found on this page")
                return False
            
            # Switch to checkbox iframe
            self.driver.switch_to.frame(checkbox_iframe)
            
            # Click the checkbox
            if not self.click_recaptcha_checkbox():
                return False
            
            # Wait a moment for potential challenge to appear
            time.sleep(2)
            
            # Check if already solved
            if self.is_recaptcha_solved():
                return True
            
            self.logger.info("Challenge appeared. Activating Buster extension...")
            
            # Switch back to main content to find challenge iframe
            self.driver.switch_to.default_content()
            
            # Find and switch to challenge iframe
            challenge_iframe = self.find_challenge_iframe()
            if not challenge_iframe:
                self.logger.error("Challenge iframe not found")
                return False
            
            self.driver.switch_to.frame(challenge_iframe)
            
            # Activate Buster extension
            if not self.activate_buster_extension():
                return False
            
            # Switch back to checkbox iframe to wait for solution
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(checkbox_iframe)
            
            # Wait for solution
            return self.wait_for_solution(max_wait_time)
            
        except Exception as e:
            self.logger.error(f"Unexpected error during reCAPTCHA solving: {str(e)}")
            return False
        
        finally:
            # Always switch back to default content
            try:
                self.driver.switch_to.default_content()
            except:
                pass

    def solve_all_recaptchas(self, max_attempts: int = 3) -> bool:
        """
        Attempt to solve all reCAPTCHAs on the current page.
        
        Args:
            max_attempts: Maximum number of attempts per reCAPTCHA
            
        Returns:
            True if all reCAPTCHAs were solved, False otherwise
        """
        attempts = 0
        while attempts < max_attempts:
            attempts += 1
            self.logger.info(f"reCAPTCHA solving attempt {attempts}/{max_attempts}")
            
            if self.solve_recaptcha():
                return True
            
            if attempts < max_attempts:
                self.logger.info("Retrying in 2 seconds...")
                time.sleep(2)
        
        self.logger.error(f"Failed to solve reCAPTCHA after {max_attempts} attempts")
        return False


# Convenience functions for common browser setups
def setup_edge_with_buster(extension_path: str, headless: bool = False) -> webdriver.Edge:
    """
    Setup Microsoft Edge with the Buster extension.
    
    Args:
        extension_path: Path to the Buster extension (.crx file)
        headless: Run in headless mode (default: False)
        
    Returns:
        Configured Edge WebDriver instance
    """
    options = webdriver.EdgeOptions()
    options.add_extension(extension_path)
    
    if not headless:
        options.add_argument("--start-maximized")
    else:
        options.add_argument("--headless")
    
    # Additional options for better compatibility
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    service = webdriver.edge.service.Service()
    return webdriver.Edge(service=service, options=options)


def setup_chrome_with_buster(extension_path: str, headless: bool = False) -> webdriver.Chrome:
    """
    Setup Google Chrome with the Buster extension.
    
    Args:
        extension_path: Path to the Buster extension (.crx file)
        headless: Run in headless mode (default: False)
        
    Returns:
        Configured Chrome WebDriver instance
    """
    options = webdriver.ChromeOptions()
    options.add_extension(extension_path)
    
    if not headless:
        options.add_argument("--start-maximized")
    else:
        options.add_argument("--headless")
    
    # Additional options for better compatibility
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    service = webdriver.chrome.service.Service()
    return webdriver.Chrome(service=service, options=options)
