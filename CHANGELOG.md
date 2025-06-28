# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-06-28

### Added
- Initial release of the generalized reCAPTCHA solver
- `RecaptchaSolver` class for automated reCAPTCHA solving
- Support for Microsoft Edge and Google Chrome browsers
- Convenience functions for browser setup with Buster extension
- Multiple retry attempts for challenging reCAPTCHAs
- Debug logging functionality
- Comprehensive error handling and timeout management
- Cross-platform compatibility (Windows, macOS, Linux)
- Detailed documentation and examples
- MIT License for open-source distribution

### Features
- **Easy Integration**: Simple API that works with existing Selenium projects
- **Cross-Browser Support**: Works with Chrome, Edge, and Chromium-based browsers  
- **Flexible Configuration**: Customizable timeouts and retry logic
- **Robust Error Handling**: Graceful handling of various failure scenarios
- **Detailed Logging**: Debug mode for troubleshooting issues
- **Multiple iframe Support**: Handles different reCAPTCHA iframe configurations

### Documentation
- Complete README with usage examples
- API reference documentation
- Example scripts demonstrating various use cases
- Installation and setup instructions
- Troubleshooting guide

### Project Structure
```
recaptcha-solver/
├── recaptcha_solver.py    # Main solver library
├── examples.py            # Usage examples
├── recaptha-solver.py     # Original script (refactored)
├── requirements.txt       # Python dependencies
├── setup.py              # Package installation
├── README.md             # Project documentation
├── LICENSE               # MIT License
├── CHANGELOG.md          # This file
├── .gitignore           # Git ignored files
└── extensions/
    └── buster.crx       # Buster extension file
```

### Technical Details
- **Python Version**: 3.7+ supported
- **Selenium Version**: 4.0.0+ required
- **Browser Support**: Chrome 90+, Edge 90+
- **Extension**: Buster CAPTCHA Solver required

### Known Limitations
- Requires Buster browser extension
- Does not work with Firefox (extension compatibility)
- Audio challenges may have lower success rates
- Some complex reCAPTCHA variants may require manual intervention

---

## Future Releases

### Planned Features
- [ ] Firefox support (pending extension compatibility)
- [ ] Headless mode improvements
- [ ] Additional CAPTCHA types support
- [ ] Performance optimizations
- [ ] Unit tests and CI/CD integration
- [ ] Docker container support
