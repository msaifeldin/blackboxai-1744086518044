import pandas as pd
from datetime import datetime

# Create sample data with more diverse patterns
data = {
    'اسم الطالب': [
        'نورة السالم', 'نورة السالم', 'نورة السالم', 'نورة السالم',  # 4 days
        'عمر الخالد',  # 1 day
        'ليلى محمد', 'ليلى محمد', 'ليلى محمد', 'ليلى محمد', 'ليلى محمد', 'ليلى محمد', 'ليلى محمد',  # 7 days
        'يوسف أحمد', 'يوسف أحمد',  # 2 days
        'سارة العلي', 'سارة العلي', 'سارة العلي'  # 3 days
    ],
    'تاريخ الغياب': [
        datetime(2024, 3, 1), datetime(2024, 3, 2), datetime(2024, 3, 3), datetime(2024, 3, 4),
        datetime(2024, 3, 1),
        datetime(2024, 3, 1), datetime(2024, 3, 2), datetime(2024, 3, 3), datetime(2024, 3, 4),
        datetime(2024, 3, 5), datetime(2024, 3, 6), datetime(2024, 3, 7),
        datetime(2024, 3, 1), datetime(2024, 3, 2),
        datetime(2024, 3, 1), datetime(2024, 3, 2), datetime(2024, 3, 3)
    ]
}

# Create DataFrame
df = pd.DataFrame(data, columns=['اسم الطالب', 'تاريخ الغياب'])

# Create Excel writer object
with pd.ExcelWriter('sample_data_2.xlsx', engine='openpyxl') as writer:
    # Write DataFrame to Excel
    df.to_excel(writer, sheet_name='غياب الطلاب', index=False, encoding='utf-8-sig')
    
    # Get workbook and worksheet objects
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

print("تم إنشاء ملف Excel الثاني بنجاح!")
print("عدد السجلات:", len(df))
print("\nتفاصيل الطلاب:")
print("- نورة السالم: 4 أيام (يتطلب رسالة تحذيرية)")
print("- عمر الخالد: يوم واحد (لا إجراء)")
print("- ليلى محمد: 7 أيام (يتطلب مراجعة المشرف)")
print("- يوسف أحمد: يومان (لا إجراء)")
print("- سارة العلي: 3 أيام (يتطلب رسالة تحذيرية)")