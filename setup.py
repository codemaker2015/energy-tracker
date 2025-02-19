from setuptools import setup, find_packages

# Define the package name
PACKAGE_NAME = "energy_tracker"

# Define the package version
VERSION = "0.2.0"

# Define the package description
DESCRIPTION = "A Python package to tracks energy consumption and CO2 emissions for LLM models and other computational tasks."

# Define the long description (optional, can be read from README.md)
with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

# Setup function to package the module
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author="Vishnu Sivan",
    author_email="codemaker2015@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/codemaker2015/energy_tracker",
    packages=find_packages(),
    install_requires=[
        "psutil",
        "pynvml",
        "codecarbon"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)