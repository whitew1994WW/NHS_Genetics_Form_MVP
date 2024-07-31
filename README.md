# NHS Genetics Test Form Submission

This is a proof of concept for a form submission system for the NHS Genetics Test. It is designed to standardise the way referrers submit forms for genetic testing. It solves the problem of inconsistent and incomplete forms being submitted to the NHS Genetics Test.

See below for a demo:
C:\Users\Will\Repos\nhs_directory\2024-07-31 22-17-44.mp4

There are two key components to this system:
- Text Mining in python: Extracting information from the test directory (pdf) using GPT-4o (one off)
- HTML/JS form: Uses the extracted information to dynamically populate the form

## Text Mining in python

In order to recreate this locally then please add your OpenAI API key to a .env file in the root directory:

```python
OPENAI_API_KEY=your_api_key
```

Then run the following commands:

```python
pip install -r requirements.txt
python extract_code_details.py
```

This will extract the information from the test directory and save it to a json file.

You then need to copy across the json file to the html form to see it updated :)
