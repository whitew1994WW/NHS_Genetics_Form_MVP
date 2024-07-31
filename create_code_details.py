import os
from openai import OpenAI
from dotenv import load_dotenv
import PyPDF2
import json
import pandas as pd


# Load in the excel data
excel_filepath = 'rare-and-inherited-disease-national-genomics-test-directory-v7.xlsx'

df = pd.read_excel(excel_filepath, sheet_name="R&ID indications", header=1)

r_codes = df["Clinical indication ID"].unique()
associated_clinical_indications = []
new_r_codes = []
for r_code in r_codes:
    associated_clinical_indications.append(df[df["Clinical indication ID"] == r_code]["Clinical Indication"].tolist()[0])
    new_r_codes.append(r_code)

r_codes = new_r_codes

code_map = dict(zip(r_codes, associated_clinical_indications))

load_dotenv()

test_directory = "national-genomic-test-directory-rare-and-inherited-disease-eligibility-criteria-v7.pdf"
output_json_file = "extracted_tests.json"
output_csv_file = "extracted_tests.csv"
prompt_file = "extract_r_code.txt"

specific_tests = r_codes[0:20] + ["R208"]


with open(prompt_file, "r") as f:
    prompt = f.read()

def run_prompt_on_extracted_text():
    client = OpenAI()


    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": extracted_text
            }
        ],
        model="gpt-4o",
    )
    return chat_completion.choices[0].message.content


# creating a pdf reader object
reader = PyPDF2.PdfReader(test_directory)

all_extracted_tests = []

for j, specific_test in enumerate(specific_tests):
    specific_test_texts = []
    for i, page in enumerate(reader.pages):
        extracted_text = page.extract_text()
        if specific_test in extracted_text:
            specific_test_texts.append((i, extracted_text))

    start_section = False
    relevant_pages = []
    for text in specific_test_texts:
        if start_section and "R" in text[1][0:40]:
            break
        if specific_test + " " in text[1][0:100]:
            start_section = True
        if start_section:
            relevant_pages.append(text)
        
    extracted_text = ' '.join([text[1] for text in relevant_pages])	

    extracted_test = run_prompt_on_extracted_text()

    extracted_test_json = json.loads(extracted_test)
    extracted_test_json["test_code"] = specific_test
    extracted_test_json["clinical_indication_name"] = specific_test + ' - ' + code_map[specific_test]

    all_extracted_tests.append(extracted_test_json)

with open(output_file, "w") as f:
    json.dump(all_extracted_tests, f)

df = pd.read_json(output_file)

df.to_csv(output_csv_file, index=False)