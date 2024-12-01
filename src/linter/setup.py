from setuptools import setup, find_packages

setup(
    name="python_linter",  # Name of your project
    version="0.1",
    packages=find_packages(),  # Automatically find packages
    entry_points={
        "console_scripts": [
            "python-linter=python_linter.__main__:main",  # Command to run your linter
        ],
    },
    install_requires=[],
    description="Custom Python Linter for VSCode",
    author="Your Name",
    author_email="your_email@example.com",
    url="https://your-project-url.com",  # Optional
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
