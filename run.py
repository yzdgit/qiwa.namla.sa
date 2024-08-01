import os
import re
import csv
from PyPDF2 import PdfReader
from openpyxl import Workbook
from flask import Flask, request, send_file, render_template_string
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Function to extract text from a single PDF
def extract_text_from_pdf(pdf_path):
    pdf_text = ""
    reader = PdfReader(pdf_path)
    number_of_pages = len(reader.pages)
    for page_num in range(number_of_pages):
        page = reader.pages[page_num]
        pdf_text += page.extract_text()
    return pdf_text

# Function to clean text (retain all characters but keep only one whitespace at a time)
def clean_text(text):
    cleaned_text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespaces with a single space
    return cleaned_text.strip()  # Remove leading/trailing whitespace

# Define strict regex patterns for each field
patterns = {
    "Name": r"Name:\s+([^\s]+(?:\s+[^\s]+)*)\s+Profession:",
    "Profession": r"Profession:\s+([^\s]+(?:\s+[^\s]+)*)\s+Employee Number:",
    "Employee Number": r"Employee Number:\s+(\d+)\s+Nationality:",
    "Nationality": r"Nationality:\s+([^\s]+)\s+Date of Birth:",
    "Date of Birth": r"Date of Birth:\s+(\d{2}-\d{2}-\d{4})\s+Identity Number:",
    "Identity Number": r"Identity Number:\s+(\d+)\s+ID Type:",
    "ID Type": r"ID Type:\s+([^\s]+(?:\s+[^\s]+)*)\s+ID Expiry Date:",
    "ID Expiry Date": r"ID Expiry Date:\s+(\d{2}-\d{2}-\d{4})\s+Gender:",
    "Gender": r"Gender:\s+([^\s]+)\s+Religion:",
    "Religion": r"Religion:\s+([^\s]+)\s+Marital Status:",
    "Marital Status": r"Marital Status:\s+([^\s]+)\s+Education:",
    "Education": r"Education:\s+([^\s]+(?:\s+[^\s]+)*)\s+Speciality:",
    "Iban": r"Iban:\s+([A-Z0-9]+)\s+Bank Name:",
    "Bank Name": r"Bank Name:\s+([^\s]+(?:\s+[^\s]+)*)\s+Email Address:",
    "Email Address": r"Email Address:\s+([^\s]+)\s+Mobile Number:",
    "Mobile Number": r"Mobile Number:\s+(\d+\s+\d+)",
    "Contract Start Date": r"starting from (\d{2}-\d{2}-\d{4})",
    "Contract End Date": r"ends in (\d{2}-\d{2}-\d{4})",
    "Joining Date": r"the second party's work is (\d{2}-\d{2}-\d{4})"
}

# Function to extract data using regex patterns
def extract_data(text, patterns):
    extracted_data = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            extracted_data[key] = match.group(1).strip()

    # Extract all monetary amounts and append to "Salary Breakdown" and "Salary Total"
    salary_pattern = re.compile(r"([0-9,\.]+) Saudi Riyals")
    salary_matches = salary_pattern.findall(text)
    if salary_matches:
        extracted_data["Salary Breakdown"] = "; ".join(salary_matches)
        salary_total = sum(float(amount.replace(',', '')) for amount in salary_matches)
        extracted_data["Salary Total"] = f"{salary_total:,.2f}"

    return extracted_data

# Function to process all PDFs in the input directory and save cleaned text to output directory
def process_pdfs(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    all_extracted_data = []

    for pdf_file in os.listdir(input_dir):
        if pdf_file.endswith('.pdf'):
            input_path = os.path.join(input_dir, pdf_file)

            pdf_text = extract_text_from_pdf(input_path)
            cleaned_text = clean_text(pdf_text)
            extracted_data = extract_data(cleaned_text, patterns)
            all_extracted_data.append(extracted_data)

    return all_extracted_data

@app.route('/', methods=['GET'])
def index():
    return render_template_string(open('templates/index.html').read())

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'pdf_files' not in request.files:
        return 'No file part', 400
    
    files = request.files.getlist('pdf_files')
    
    if len(files) == 0:
        return 'No selected file', 400
    
    if len(files) > 10:
        return 'Too many files. Maximum is 10.', 400

    input_directory = 'temp_input'
    output_directory = 'temp_output'
    
    os.makedirs(input_directory, exist_ok=True)
    os.makedirs(output_directory, exist_ok=True)

    for file in files:
        if file.filename == '':
            return 'No selected file', 400
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(input_directory, filename))

    extracted_data = process_pdfs(input_directory, output_directory)

    xlsx_output_path = os.path.join(output_directory, 'extracted_data.xlsx')
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Extracted Data'

    fieldnames = list(patterns.keys()) + ["Salary Breakdown", "Salary Total"]
    sheet.append(fieldnames)

    for data in extracted_data:
        row = [f'{data.get(field, "")}' for field in fieldnames]
        sheet.append(row)

    workbook.save(xlsx_output_path)

    # Clean up temporary directories
    for file in os.listdir(input_directory):
        os.remove(os.path.join(input_directory, file))
    os.rmdir(input_directory)

    return '''
    <div class="bg-white overflow-hidden shadow rounded-lg max-w-lg mx-auto">
        <div class="px-4 py-5 sm:p-6">
            <div class="text-center">
                <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100">
                    <svg class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                </div>
                <h3 class="mt-2 text-lg font-medium text-gray-900">
                    PDFs processed successfully!
                </h3>
                <p class="mt-2 text-sm text-gray-500">
                    Your Excel file is ready for download.
                </p>
                <div class="mt-4">
                    <a href="/download" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                        Download Excel File
                    </a>
                </div>
            </div>
        </div>
    </div>
    '''

@app.route('/download')
def download_file():
    path = "temp_output/extracted_data.xlsx"
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
