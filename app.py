from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
import pandas as pd
import os
import traceback

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# Create upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def determine_procedure(absence_count):
    if absence_count <= 2:
        return "لا إجراء", "لا يوجد رسالة"
    elif absence_count <= 5:
        return "إرسال رسالة تحذيرية", f"نود إعلامكم بأن ابنكم/ابنتكم تغيب/ت لمدة {absence_count} أيام. نرجو الالتزام بالحضور المدرسي."
    else:
        return "مراجعة المشرف والأخصائي الاجتماعي", f"نود إعلامكم بأن ابنكم/ابنتكم تغيب/ت لمدة {absence_count} أيام. نرجو الحضور للمدرسة لمناقشة هذا الأمر."

def process_absence_data(filepath):
    try:
        print(f"Reading Excel file from: {filepath}")
        
        # Read Excel file
        df = pd.read_excel(filepath)
        print(f"Excel file read successfully. Columns: {df.columns.tolist()}")
        
        # Validate required columns
        required_columns = ["رقم الطالب", "اسم الطالب", "الشعبة", "غائب"]
        for col in required_columns:
            if col not in df.columns:
                error_msg = f"العمود المطلوب '{col}' غير موجود في الملف. الأعمدة الموجودة: {', '.join(df.columns)}"
                print(f"Error: {error_msg}")
                raise ValueError(error_msg)

        print(f"Data shape before processing: {df.shape}")
        
        # Filter only absent students (where غائب column is True or 1)
        absent_students = df[df['غائب'] == 1].copy()
        
        # Group by student and count absences
        absence_counts = absent_students.groupby(["رقم الطالب", "اسم الطالب", "الشعبة"]).size().reset_index(name="عدد ايام الغياب")
        print(f"Grouped data shape: {absence_counts.shape}")
        
        # Apply business rules for each student
        results = []
        for _, row in absence_counts.iterrows():
            procedure, message = determine_procedure(row["عدد ايام الغياب"])
            results.append({
                "رقم الطالب": row["رقم الطالب"],
                "اسم الطالب": row["اسم الطالب"],
                "الشعبة": row["الشعبة"],
                "عدد ايام الغياب": row["عدد ايام الغياب"],
                "الإجراء المتبع": procedure,
                "الرسالة المقترحة": message
            })
        
        result_df = pd.DataFrame(results)
        print(f"Final results shape: {result_df.shape}")  # Debug print
        print("Sample of results:")  # Debug print
        print(result_df.head())  # Debug print
        
        return result_df
        
    except pd.errors.EmptyDataError:
        error_msg = "الملف فارغ أو لا يحتوي على بيانات"
        print(f"Error: {error_msg}")  # Debug print
        raise Exception(error_msg)
    except Exception as e:
        error_msg = f"حدث خطأ أثناء معالجة الملف: {str(e)}"
        print(f"Error: {error_msg}")  # Debug print
        print(f"Traceback: {traceback.format_exc()}")  # Debug print
        raise Exception(error_msg)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            print("POST request received")  # Debug print
            print(f"Files in request: {request.files}")  # Debug print
            print(f"Form data: {request.form}")  # Debug print
            
            # Check if a file was uploaded
            if 'file' not in request.files:
                print("No file part in request")  # Debug print
                flash('لم يتم اختيار ملف')
                return redirect(request.url)
                
            file = request.files['file']
            print(f"Received file: {file.filename}")  # Debug print
            
            # If no file selected
            if file.filename == '':
                print("No selected file")  # Debug print
                flash('لم يتم اختيار ملف')
                return redirect(request.url)
                
            if file and allowed_file(file.filename):
                try:
                    # Create a unique filename
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    original_filename = secure_filename(file.filename)
                    filename = f"upload_{timestamp}_{original_filename}"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    
                    print(f"Original filename: {original_filename}")  # Debug print
                    print(f"Saving file to: {filepath}")  # Debug print
                    
                    # Ensure uploads directory exists with proper permissions
                    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                    os.chmod(app.config['UPLOAD_FOLDER'], 0o777)
                    
                    # Save the file
                    file.save(filepath)
                    print(f"File saved successfully. File exists: {os.path.exists(filepath)}, Size: {os.path.getsize(filepath)}")  # Debug print
                    
                    if not os.path.exists(filepath):
                        raise Exception("File was not saved successfully")
                    
                    # Process the file
                    print(f"Processing file: {filepath}")  # Debug print
                    results = process_absence_data(filepath)
                    print("File processed successfully")  # Debug print
                    
                    # Remove the file after processing
                    if os.path.exists(filepath):
                        os.remove(filepath)
                        print("Temporary file removed")  # Debug print
                    
                    # Render results
                    return render_template('result.html', results=results.to_dict('records'))
                    
                except Exception as e:
                    print(f"Error processing file: {str(e)}")  # Debug print
                    print(f"Traceback: {traceback.format_exc()}")  # Debug print
                    flash(f'حدث خطأ أثناء معالجة الملف: {str(e)}')
                    return redirect(request.url)
                finally:
                    # Ensure file is removed even if an error occurs
                    if os.path.exists(filepath):
                        os.remove(filepath)
                        print("Temporary file removed in finally block")  # Debug print
            else:
                print(f"Invalid file type: {file.filename}")  # Debug print
                flash('نوع الملف غير مسموح به. يرجى استخدام ملف Excel (.xlsx, .xls)')
                return redirect(request.url)
        except Exception as e:
            print(f"Unexpected error: {str(e)}")  # Debug print
            print(f"Traceback: {traceback.format_exc()}")  # Debug print
            flash(f'حدث خطأ غير متوقع: {str(e)}')
            return redirect(request.url)
            
    return render_template('index.html')

@app.errorhandler(413)
def too_large(e):
    flash('حجم الملف كبير جداً. الحد الأقصى المسموح به هو 16 ميجابايت')
    return redirect(url_for('upload_file'))

if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')