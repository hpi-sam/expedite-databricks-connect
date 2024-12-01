# Python Linter

## Overview

This is a Python-based linter designed to analyze your code for errors, style issues, and best practices. Use it to maintain clean, readable, and Pythonic code in your projects.

---

## Usage

Follow these steps to install set up and run the Python Linter with your python file:

1. **Install Required Dependencies**  
   Run the following command to install all dependencies listed in `requirements.txt` and install the linter as a python package:
   ```bash
   pip install -r requirements.txt
   pip install -e . 

   #To run the Linter with a python file as command line argument (Example Usage): 
   python python_linter/__main__.py file_to_lint.py

   #General usage: 
   python __main__.py [YOURPYTHONFILE]
