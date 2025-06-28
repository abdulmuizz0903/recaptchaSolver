"""
Testing script for reCAPTCHA Solver

This script provides comprehensive testing functionality for the reCAPTCHA solver
including unit tests, integration tests, and manual testing scenarios.

Author: Abdul Muizz
"""

import os
import sys
import time
import unittest
from unittest.mock import Mock, patch, MagicMock
import logging

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from recaptcha_solver import RecaptchaSolver, setup_edge_with_buster, setup_chrome_with_buster
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
except ImportError as e:
    print(f"Import error: {e}")
    print("Please install required dependencies: pip install -r requirements.txt")
    sys.exit(1)


class TestRecaptchaSolver(unittest.TestCase):
    """Unit tests for RecaptchaSolver class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_driver = Mock()
        self.mock_wait = Mock()
        
        # Mock WebDriverWait
        with patch('recaptcha_solver.WebDriverWait') as mock_webdriver_wait:
            mock_webdriver_wait.return_value = self.mock_wait
            self.solver = RecaptchaSolver(self.mock_driver, timeout=10, debug=False)
    
    def test_solver_initialization(self):
        """Test solver initialization with different parameters"""
        # Test default parameters
        with patch('recaptcha_solver.WebDriverWait'):
            solver = RecaptchaSolver(self.mock_driver)
            self.assertEqual(solver.timeout, 20)
            self.assertIsNotNone(solver.logger)
    
    def test_handle_extension_tabs_single_tab(self):
        """Test handling extension tabs with single tab"""
        self.mock_driver.window_handles = ['tab1']
        
        # Should not switch tabs if only one tab exists
        self.solver.handle_extension_tabs()
        self.mock_driver.switch_to.window.assert_not_called()
    
    def test_handle_extension_tabs_multiple_tabs(self):
        """Test handling extension tabs with multiple tabs"""
        self.mock_driver.window_handles = ['tab1', 'tab2', 'tab3']
        
        # Should switch back to the first tab
        self.solver.handle_extension_tabs()
        self.mock_driver.switch_to.window.assert_called_once_with('tab1')
    
    def test_find_recaptcha_checkbox_iframe_success(self):
        """Test finding reCAPTCHA checkbox iframe successfully"""
        mock_iframe = Mock()
        self.mock_wait.until.return_value = mock_iframe
        
        result = self.solver.find_recaptcha_checkbox_iframe()
        self.assertEqual(result, mock_iframe)
        self.mock_wait.until.assert_called_once()
    
    def test_find_recaptcha_checkbox_iframe_timeout(self):
        """Test finding reCAPTCHA checkbox iframe with timeout"""
        self.mock_wait.until.side_effect = TimeoutException()
        
        result = self.solver.find_recaptcha_checkbox_iframe()
        self.assertIsNone(result)
    
    def test_is_recaptcha_solved_true(self):
        """Test checking if reCAPTCHA is solved (true case)"""
        mock_element = Mock()
        self.mock_driver.find_element.return_value = mock_element
        
        result = self.solver.is_recaptcha_solved()
        self.assertTrue(result)
    
    def test_is_recaptcha_solved_false(self):
        """Test checking if reCAPTCHA is solved (false case)"""
        self.mock_driver.find_element.side_effect = NoSuchElementException()
        
        result = self.solver.is_recaptcha_solved()
        self.assertFalse(result)


class IntegrationTest:
    """Integration tests that require actual browser and extension"""
    
    def __init__(self):
        self.extension_path = os.path.abspath("extensions/buster.crx")
        self.test_url = "https://patrickhlauke.github.io/recaptcha/"
        self.results = {}
    
    def check_prerequisites(self):
        """Check if all prerequisites are available"""
        print("🔍 Checking prerequisites...")
        
        issues = []
        
        # Check if extension exists
        if not os.path.exists(self.extension_path):
            issues.append(f"❌ Buster extension not found at: {self.extension_path}")
        else:
            print(f"✅ Buster extension found at: {self.extension_path}")
        
        # Check if we can create a webdriver
        try:
            options = webdriver.EdgeOptions()
            options.add_argument("--headless")
            driver = webdriver.Edge(options=options)
            driver.quit()
            print("✅ Edge WebDriver available")
        except Exception as e:
            issues.append(f"❌ Edge WebDriver not available: {str(e)}")
        
        return issues
    
    def test_browser_setup_edge(self):
        """Test Edge browser setup with Buster extension"""
        print("\n🧪 Testing Edge browser setup...")
        
        try:
            driver = setup_edge_with_buster(self.extension_path, headless=True)
            
            # Basic functionality test
            driver.get("https://www.google.com")
            title = driver.title
            
            driver.quit()
            
            self.results['edge_setup'] = {
                'status': 'PASS',
                'message': f'Edge setup successful, loaded page: {title}'
            }
            print("✅ Edge setup test passed")
            
        except Exception as e:
            self.results['edge_setup'] = {
                'status': 'FAIL',
                'message': f'Edge setup failed: {str(e)}'
            }
            print(f"❌ Edge setup test failed: {str(e)}")
    
    def test_browser_setup_chrome(self):
        """Test Chrome browser setup with Buster extension"""
        print("\n🧪 Testing Chrome browser setup...")
        
        try:
            driver = setup_chrome_with_buster(self.extension_path, headless=True)
            
            # Basic functionality test
            driver.get("https://www.google.com")
            title = driver.title
            
            driver.quit()
            
            self.results['chrome_setup'] = {
                'status': 'PASS',
                'message': f'Chrome setup successful, loaded page: {title}'
            }
            print("✅ Chrome setup test passed")
            
        except Exception as e:
            self.results['chrome_setup'] = {
                'status': 'FAIL',
                'message': f'Chrome setup failed: {str(e)}'
            }
            print(f"❌ Chrome setup test failed: {str(e)}")
    
    def test_recaptcha_detection(self):
        """Test reCAPTCHA detection on test page"""
        print("\n🧪 Testing reCAPTCHA detection...")
        
        try:
            driver = setup_edge_with_buster(self.extension_path, headless=True)
            solver = RecaptchaSolver(driver, debug=False)
            
            driver.get(self.test_url)
            time.sleep(3)  # Wait for page load
            
            # Test if we can find the reCAPTCHA iframe
            iframe = solver.find_recaptcha_checkbox_iframe()
            
            driver.quit()
            
            if iframe:
                self.results['recaptcha_detection'] = {
                    'status': 'PASS',
                    'message': 'reCAPTCHA iframe detected successfully'
                }
                print("✅ reCAPTCHA detection test passed")
            else:
                self.results['recaptcha_detection'] = {
                    'status': 'FAIL',
                    'message': 'reCAPTCHA iframe not found'
                }
                print("❌ reCAPTCHA detection test failed")
                
        except Exception as e:
            self.results['recaptcha_detection'] = {
                'status': 'FAIL',
                'message': f'reCAPTCHA detection failed: {str(e)}'
            }
            print(f"❌ reCAPTCHA detection test failed: {str(e)}")
    
    def test_full_recaptcha_solve(self):
        """Test full reCAPTCHA solving process"""
        print("\n🧪 Testing full reCAPTCHA solving process...")
        print("⚠️  This test will open a visible browser window for 30 seconds")
        
        try:
            driver = setup_edge_with_buster(self.extension_path, headless=False)
            solver = RecaptchaSolver(driver, debug=True)
            
            driver.get(self.test_url)
            print("🌐 Navigated to test page")
            
            # Attempt to solve the reCAPTCHA
            success = solver.solve_recaptcha(max_wait_time=25)
            
            if success:
                self.results['full_solve'] = {
                    'status': 'PASS',
                    'message': 'reCAPTCHA solved successfully'
                }
                print("✅ Full reCAPTCHA solve test passed!")
            else:
                self.results['full_solve'] = {
                    'status': 'FAIL',
                    'message': 'reCAPTCHA solving failed'
                }
                print("❌ Full reCAPTCHA solve test failed")
            
            print("⏳ Keeping browser open for 5 seconds to verify result...")
            time.sleep(5)
            driver.quit()
            
        except Exception as e:
            self.results['full_solve'] = {
                'status': 'FAIL',
                'message': f'Full solve test failed: {str(e)}'
            }
            print(f"❌ Full reCAPTCHA solve test failed: {str(e)}")
    
    def run_all_tests(self):
        """Run all integration tests"""
        print("🚀 Starting Integration Tests")
        print("=" * 50)
        
        # Check prerequisites first
        issues = self.check_prerequisites()
        if issues:
            print("\n❌ Prerequisites not met:")
            for issue in issues:
                print(f"   {issue}")
            return False
        
        # Run tests
        self.test_browser_setup_edge()
        self.test_browser_setup_chrome()
        self.test_recaptcha_detection()
        
        # Ask user if they want to run the full solve test
        print("\n" + "=" * 50)
        response = input("🤔 Do you want to run the full reCAPTCHA solve test? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            self.test_full_recaptcha_solve()
        else:
            print("⏭️  Skipping full solve test")
        
        # Print summary
        self.print_summary()
        
        return True
    
    def print_summary(self):
        """Print test results summary"""
        print("\n" + "=" * 50)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 50)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for result in self.results.values() if result['status'] == 'PASS')
        failed_tests = total_tests - passed_tests
        
        for test_name, result in self.results.items():
            status_emoji = "✅" if result['status'] == 'PASS' else "❌"
            print(f"{status_emoji} {test_name.replace('_', ' ').title()}: {result['message']}")
        
        print("\n" + "-" * 50)
        print(f"📈 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📊 Success Rate: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "No tests run")


def manual_test_interactive():
    """Interactive manual testing"""
    print("\n🎮 Interactive Manual Testing")
    print("=" * 40)
    
    extension_path = os.path.abspath("extensions/buster.crx")
    
    if not os.path.exists(extension_path):
        print(f"❌ Extension not found at: {extension_path}")
        return
    
    print("Available test options:")
    print("1. Test on reCAPTCHA demo page")
    print("2. Test on custom URL")
    print("3. Multiple attempt test")
    print("4. Debug mode test")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        test_demo_page(extension_path)
    elif choice == "2":
        test_custom_url(extension_path)
    elif choice == "3":
        test_multiple_attempts(extension_path)
    elif choice == "4":
        test_debug_mode(extension_path)
    else:
        print("❌ Invalid choice")


def test_demo_page(extension_path):
    """Test on the demo page"""
    print("\n🧪 Testing on reCAPTCHA demo page...")
    
    driver = setup_edge_with_buster(extension_path)
    solver = RecaptchaSolver(driver, debug=True)
    
    try:
        driver.get("https://patrickhlauke.github.io/recaptcha/")
        print("✅ Navigated to demo page")
        
        success = solver.solve_recaptcha()
        
        if success:
            print("🎉 reCAPTCHA solved successfully!")
        else:
            print("❌ Failed to solve reCAPTCHA")
        
        input("Press Enter to close browser...")
        
    finally:
        driver.quit()


def test_custom_url(extension_path):
    """Test on a custom URL"""
    url = input("Enter the URL to test: ").strip()
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    print(f"\n🧪 Testing on custom URL: {url}")
    
    driver = setup_edge_with_buster(extension_path)
    solver = RecaptchaSolver(driver, debug=True)
    
    try:
        driver.get(url)
        print("✅ Navigated to custom URL")
        
        input("Navigate to the page with reCAPTCHA and press Enter to continue...")
        
        success = solver.solve_recaptcha()
        
        if success:
            print("🎉 reCAPTCHA solved successfully!")
        else:
            print("❌ Failed to solve reCAPTCHA")
        
        input("Press Enter to close browser...")
        
    finally:
        driver.quit()


def test_multiple_attempts(extension_path):
    """Test multiple attempts"""
    print("\n🧪 Testing multiple attempts...")
    
    driver = setup_edge_with_buster(extension_path)
    solver = RecaptchaSolver(driver, debug=True)
    
    try:
        driver.get("https://patrickhlauke.github.io/recaptcha/")
        print("✅ Navigated to demo page")
        
        success = solver.solve_all_recaptchas(max_attempts=3)
        
        if success:
            print("🎉 reCAPTCHA solved with multiple attempts!")
        else:
            print("❌ Failed to solve reCAPTCHA after multiple attempts")
        
        input("Press Enter to close browser...")
        
    finally:
        driver.quit()


def test_debug_mode(extension_path):
    """Test with detailed debug output"""
    print("\n🧪 Testing with debug mode enabled...")
    
    # Enable detailed logging
    logging.basicConfig(level=logging.DEBUG)
    
    driver = setup_edge_with_buster(extension_path)
    solver = RecaptchaSolver(driver, debug=True)
    
    try:
        driver.get("https://patrickhlauke.github.io/recaptcha/")
        print("✅ Navigated to demo page with debug logging")
        
        success = solver.solve_recaptcha()
        
        if success:
            print("🎉 reCAPTCHA solved successfully (debug mode)!")
        else:
            print("❌ Failed to solve reCAPTCHA (debug mode)")
        
        input("Press Enter to close browser...")
        
    finally:
        driver.quit()


def main():
    """Main testing function"""
    print("🧪 reCAPTCHA Solver Testing Suite")
    print("=" * 50)
    print("Created by: Abdul Muizz")
    print("=" * 50)
    
    print("\nSelect testing mode:")
    print("1. Unit Tests")
    print("2. Integration Tests")
    print("3. Interactive Manual Tests")
    print("4. Run All Tests")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        print("\n🧪 Running Unit Tests...")
        unittest.main(argv=[''], exit=False, verbosity=2)
        
    elif choice == "2":
        print("\n🧪 Running Integration Tests...")
        integration_test = IntegrationTest()
        integration_test.run_all_tests()
        
    elif choice == "3":
        manual_test_interactive()
        
    elif choice == "4":
        print("\n🧪 Running All Tests...")
        print("\n1️⃣ Unit Tests:")
        unittest.main(argv=[''], exit=False, verbosity=1)
        
        print("\n2️⃣ Integration Tests:")
        integration_test = IntegrationTest()
        integration_test.run_all_tests()
        
        print("\n3️⃣ Manual Test Available - Run script again and select option 3")
        
    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    main()
