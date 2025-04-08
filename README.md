
Built by https://www.blackbox.ai

---

```markdown
# Student Absence Management System

## Project Overview
The Student Absence Management System is a web application built using Flask that allows users to upload Excel files containing student absence data, process that data, and generate actionable messages based on each student's absence record. The application facilitates efficient communication between educational institutions and parents regarding student attendance.

## Installation
To run this project locally, ensure that you have Python installed on your machine. Then follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repository/student-absence-management.git
   cd student-absence-management
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```
   The application will start on `http://127.0.0.1:8000/`.

## Usage
- Navigate to the application in your web browser.
- Upload an Excel file containing student absence data. The file should have the following columns:
  - `رقم الطالب` (Student ID)
  - `اسم الطالب` (Student Name)
  - `الشعبة` (Class)
  - `غائب` (Absent: 1 for absent, 0 for present)
- After processing, the application will display results outlining the number of absence days for each student and the corresponding suggested actions/messages.

## Features
- User-friendly interface for file uploads.
- Supports Excel files of .xlsx and .xls format.
- Displays results with tailored messages based on absence counts.
- Handles errors with meaningful messages to the user.
- Maintains file management by removing temporary files after processing.

## Dependencies
This project requires the following Python packages, mentioned in `requirements.txt`:
- Flask
- pandas
- openpyxl
- werkzeug

## Project Structure
```
student-absence-management/
│
├── app.py                      # Main application file, handles routes and file processing
├── create_excel.py             # Script to generate sample Excel file for testing
├── create_excel_example2.py     # Script to create another sample Excel file for testing with diverse patterns
├── requirements.txt             # Lists all the required packages and their versions
├── uploads/                     # Directory where uploaded Excel files are temporarily stored
├── templates/                   # Directory containing HTML files for rendering results
│   ├── index.html              # Home page for file uploads
│   └── result.html             # Page for displaying processed results
└── README.md                   # Project overview and documentation
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
```