# Qiwa Contracts to Excel converter

## About
Qiwa Contracts to Excel is an open-source web application that allows users to bulk convert Qiwa Contracts (in PDF format) into a single, organized Excel file. This tool streamlines the process of extracting and collating information from multiple employment contracts, making it easier for HR professionals, managers, and employees to manage and analyze contract data.

## Features
- Upload multiple Qiwa Contract PDFs (up to 10 files, max 1MB each)
- Extract key information from contracts, including:
  - Employee details (Name, Profession, Employee Number, etc.)
  - Contract dates
  - Salary information
- Compile extracted data into a single, well-organized Excel file
- User-friendly web interface
- Secure processing: files are processed locally and not stored long-term

## Tech Stack
- Backend: Python with Flask
- PDF Processing: PyPDF2
- Excel Generation: openpyxl
- Frontend: HTML, Tailwind CSS, and HTMX

## Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Git

### Steps
1. Clone the repository:
   ```
   git clone https://github.com/yzdgit/qiwa-parser.git
   cd qiwa-contracts-to-excel
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open your web browser and navigate to `http://localhost:8080`

## Usage
1. Access the web application through your browser.
2. Click on "Upload PDFs" or drag and drop your Qiwa Contract PDFs (up to 10 files, max 1MB each).
3. Click "Process PDFs" to start the conversion.
4. Once processing is complete, click "Download Excel File" to get your compiled data.

## Contributing
We welcome contributions to the Qiwa Contracts to Excel project! Here's how you can contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with a clear, descriptive commit message.
4. Push your changes to your fork.
5. Submit a pull request to the main repository.

Please ensure your code adheres to the project's coding standards and includes appropriate tests.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer
This tool is not officially affiliated with or endorsed by Qiwa or any government entity. It is an independent, open-source project designed to assist with contract management. Users are responsible for ensuring their use of this tool complies with all relevant laws and regulations.

## Support
If you encounter any issues or have questions, please file an issue on the GitHub issue tracker.

## Acknowledgements
- Special thanks to the open-source community for providing the libraries and tools that make this project possible.

