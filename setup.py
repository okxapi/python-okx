import os
import setuptools

# Get the directory where setup.py is located
HERE = os.path.dirname(os.path.abspath(__file__))

# Read version from package
import okx

# Read README
with open(os.path.join(HERE, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()


def parse_requirements():
    """Parse requirements from requirements.txt."""
    requirements = []
    req_path = os.path.join(HERE, "requirements.txt")
    
    if not os.path.exists(req_path):
        return requirements
    
    with open(req_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue
            # Handle inline comments
            if "#" in line:
                line = line.split("#")[0].strip()
            requirements.append(line)
    
    return requirements


setuptools.setup(
    name="python-okx",
    version=okx.__version__,
    author="okxv5api",
    author_email="api@okg.com",
    description="Python SDK for OKX",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://okx.com/docs-v5/",
    packages=setuptools.find_packages(exclude=["test", "test.*", "example"]),
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=parse_requirements(),
)
