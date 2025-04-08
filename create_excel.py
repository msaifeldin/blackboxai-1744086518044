import pandas as pd
from datetime import datetime

# Create sample data with explicit column names
data = {
    'اسم الطالب': [
        'أحمد محمد', 'أحمد محمد',
        'سارة أحمد',
        'خالد عبدالله', 'خالد عبدالله', 'خالد عبدالله', 'خالد عبدالله', 'خالد عبدالله', 'خالد عبدالله',
        'محمد علي',
        'فاطمة حسن', 'فاطمة حسن', 'فاطمة حسن'
    ],
    'تاريخ الغياب': [
        datetime(2024, 3, 1), datetime(2024, 3, 2),
        datetime(2024, 3, 1),
        datetime(2024, 3, 1), datetime(2024, 3, 2), datetime(2024, 3, 3),
        datetime(2024, 3, 4), datetime(2024, 3, 5), datetime(2024, 3, 6),
        datetime(2024, 3, 1),
        datetime(2024, 3, 1), datetime(2024, 3, 2), datetime(2024, 3, 3)
    ]
}

# Create DataFrame with explicit column names
df = pd.DataFrame(data, columns=['اسم الطالب', 'تاريخ الغياب'])

# Create Excel writer object with openpyxl engine
with pd.ExcelWriter('sample_data.xlsx', engine='openpyxl') as writer:
    # Write the DataFrame to Excel with explicit column names
    df.to_excel(writer, sheet_name='غياب الطلاب', index=False, encoding='utf-8-sig')
    
    # Get the workbook and worksheet objects
    workbook = writer.book
    worksheet = writer.sheets['غياب الطلاب']
    
    # Auto-adjust columns' width
    for column in worksheet.columns:
        max_length = 0
        column = [cell for cell in column]
        try:
            max_length = max(len(str(cell.value)) for cell in column if cell.value)
            adjusted_width = (max_length + 2)
            worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
        except:
            pass

print("تم إنشاء ملف Excel بنجاح!")
print("عدد السجلات:", len(df))
print("الأعمدة:", df.columns.tolist())