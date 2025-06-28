from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="recaptcha-solver",
    version="1.0.0",
    author="reCAPTCHA Solver Contributors",
    author_email="",
    description="A Python library for automatically solving reCAPTCHAs using Selenium and Buster extension",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/recaptcha-solver",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    keywords="recaptcha, selenium, automation, captcha, solver, buster",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/recaptcha-solver/issues",
        "Source": "https://github.com/yourusername/recaptcha-solver",
    },
)
