# reCAPTCHA Solver

A Python library for automatically solving reCAPTCHAs using the Buster browser extension and Selenium WebDriver. This tool can be integrated into any web automation project to handle reCAPTCHA challenges seamlessly.

## Features

- 🔧 **Easy Integration**: Simple API that works with any existing Selenium project
- 🌐 **Cross-Browser Support**: Works with Chrome, Edge, and other Chromium-based browsers
- 🎯 **Multiple Attempts**: Configurable retry logic for challenging reCAPTCHAs
- 📝 **Detailed Logging**: Debug mode for troubleshooting
- 🚀 **High Success Rate**: Uses the proven Buster extension for solving
- 🔄 **Flexible**: Handles various reCAPTCHA iframe configurations

## Prerequisites

- Python 3.7 or higher
- Selenium WebDriver
- Buster browser extension (.crx file)
- Chrome/Edge browser and corresponding WebDriver

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/recaptcha-solver.git
cd recaptcha-solver
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download the Buster extension:
   - Visit the [Buster extension page](https://chrome.google.com/webstore/detail/buster-captcha-solver-for/mpbjkejclgfgadiemmefgebjfooflfhl)
   - Download the .crx file and place it in the `extensions/` folder

4. Test the installation:
```bash
python test_recaptcha_solver.py
```

## Quick Start

```python
from recaptcha_solver import RecaptchaSolver, setup_edge_with_buster
import os

# Setup browser with Buster extension
extension_path = os.path.abspath("extensions/buster.crx")
driver = setup_edge_with_buster(extension_path)

try:
    # Create solver instance
    solver = RecaptchaSolver(driver, debug=True)
    
    # Navigate to your target page
    driver.get("https://example.com")
    
    # Solve any reCAPTCHAs on the page
    if solver.solve_recaptcha():
        print("✅ reCAPTCHA solved successfully!")
        # Continue with your automation...
    else:
        print("❌ Failed to solve reCAPTCHA")
        
finally:
    driver.quit()
```

## API Reference

### RecaptchaSolver Class

#### Constructor
```python
RecaptchaSolver(driver, timeout=20, debug=False)
```

- `driver`: Selenium WebDriver instance (must have Buster extension installed)
- `timeout`: Maximum time to wait for elements (default: 20 seconds)
- `debug`: Enable debug logging (default: False)

#### Methods

##### `solve_recaptcha(max_wait_time=30)`
Solves a single reCAPTCHA on the current page.

**Parameters:**
- `max_wait_time`: Maximum time to wait for Buster to solve the challenge

**Returns:** `bool` - True if successful, False otherwise

##### `solve_all_recaptchas(max_attempts=3)`
Attempts to solve all reCAPTCHAs with retry logic.

**Parameters:**
- `max_attempts`: Maximum number of attempts per reCAPTCHA

**Returns:** `bool` - True if all reCAPTCHAs were solved, False otherwise

### Convenience Functions

#### `setup_edge_with_buster(extension_path, headless=False)`
Sets up Microsoft Edge with the Buster extension pre-installed.

#### `setup_chrome_with_buster(extension_path, headless=False)`
Sets up Google Chrome with the Buster extension pre-installed.

## Examples

### Basic Usage
```python
from recaptcha_solver import RecaptchaSolver, setup_edge_with_buster

# Setup
driver = setup_edge_with_buster("extensions/buster.crx")
solver = RecaptchaSolver(driver)

# Navigate and solve
driver.get("https://example.com")
success = solver.solve_recaptcha()
```

### Integration with Existing Code
```python
# Your existing WebDriver setup
from selenium import webdriver
from recaptcha_solver import RecaptchaSolver

# Add Buster extension to your existing options
options = webdriver.EdgeOptions()
options.add_extension("extensions/buster.crx")
driver = webdriver.Edge(options=options)

# Use the solver when you encounter reCAPTCHA
solver = RecaptchaSolver(driver)
if solver.solve_recaptcha():
    # Continue with your automation
    pass
```

### Multiple Attempts with Error Handling
```python
from recaptcha_solver import RecaptchaSolver, setup_edge_with_buster

driver = setup_edge_with_buster("extensions/buster.crx")
solver = RecaptchaSolver(driver, timeout=15, debug=True)

try:
    driver.get("https://example.com")
    
    # Try up to 3 times
    if solver.solve_all_recaptchas(max_attempts=3):
        print("Success!")
    else:
        print("Failed after multiple attempts")
        
except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()
```

### Run Example Scripts
The project includes comprehensive examples and testing:

```bash
# Run the original refactored script
python recaptha-solver.py

# Run example scenarios
python examples.py

# Run comprehensive tests
python test_recaptcha_solver.py
```

## How It Works

1. **Detection**: The solver automatically detects reCAPTCHA iframes on the page
2. **Checkbox Click**: Clicks the reCAPTCHA checkbox to trigger the challenge
3. **Challenge Handling**: If a challenge appears, switches to the challenge iframe
4. **Smart Delay**: Waits 5 seconds before activating Buster for optimal results
5. **Buster Activation**: Locates and clicks the Buster extension button
6. **Verification**: Waits for the reCAPTCHA to be marked as solved

## Testing

The project includes a comprehensive testing suite:

### Run Tests
```bash
python test_recaptcha_solver.py
```

### Test Options
1. **Unit Tests** - Test individual components
2. **Integration Tests** - Test with real browsers
3. **Interactive Manual Tests** - Step-by-step testing
4. **Run All Tests** - Comprehensive testing

### Test Features
- ✅ Prerequisite validation
- ✅ Browser setup testing
- ✅ reCAPTCHA detection testing
- ✅ Full solving process testing
- ✅ Cross-browser compatibility testing

## Troubleshooting

### Common Issues

1. **Extension not found**: Ensure the Buster extension (.crx file) is in the correct path
2. **Timeout errors**: Increase the timeout value or check your internet connection
3. **No reCAPTCHA found**: The page might not have a reCAPTCHA or it's not loaded yet

### Debug Mode

Enable debug logging to see detailed information:
```python
solver = RecaptchaSolver(driver, debug=True)
```

### Browser Compatibility

- ✅ Microsoft Edge (Recommended)
- ✅ Google Chrome
- ✅ Chromium-based browsers
- ❌ Firefox (Extension compatibility issues)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the test suite: `python test_recaptcha_solver.py`
5. Add tests if applicable
6. Submit a pull request

### Project Structure

```
recaptcha-solver/
├── recaptcha_solver.py       # 🎯 Main solver library
├── examples.py              # 📚 Usage examples and demos
├── test_recaptcha_solver.py # 🧪 Comprehensive test suite
├── recaptha-solver.py       # 🔄 Original script (refactored)
├── requirements.txt         # 📋 Python dependencies
├── setup.py                # 🛠️ Package installation
├── README.md               # 📖 This documentation
├── LICENSE                 # ⚖️ MIT License
├── CHANGELOG.md            # 📝 Version history
├── .gitignore             # 🚫 Git ignored files
└── extensions/
    └── buster.crx         # 🧩 Buster extension
```

## Legal Notice

This tool is for educational and testing purposes only. Please ensure you comply with the terms of service of any websites you interact with. The authors are not responsible for any misuse of this software.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

### Special Thanks to Buster 🙏

This project is built upon the excellent work of the **[Buster: Captcha Solver for Humans](https://github.com/dessant/buster)** browser extension. Buster is the core technology that makes this reCAPTCHA solver possible.

**About Buster:**
- 🧩 An open-source browser extension for solving CAPTCHAs
- 🤖 Uses advanced audio recognition and machine learning
- 🌟 Maintained by [dessant](https://github.com/dessant)
- 🔗 Repository: https://github.com/dessant/buster/tree/main

**Why Buster?**
Buster provides a reliable, ethical solution for CAPTCHA solving by using accessibility features (audio challenges) rather than bypassing security measures. This makes it both effective and respectful of website security policies.

### Other Acknowledgments

- [Selenium WebDriver](https://selenium.dev/) team for the automation framework
- The open-source community for continuous improvements and feedback

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/recaptcha-solver/issues) page
2. Review the examples in `examples.py`
3. Run the test suite: `python test_recaptcha_solver.py`
4. Enable debug mode for detailed logs: `RecaptchaSolver(driver, debug=True)`
5. Create a new issue with your problem description

### Quick Debugging

```python
# Enable comprehensive logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Create solver with debug mode
solver = RecaptchaSolver(driver, debug=True, timeout=30)

# Run tests to verify setup
python test_recaptcha_solver.py
```

---
  
**Star ⭐ this repository if you find it useful!**
