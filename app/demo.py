import pandas as pd


import re


import pandas as pd
import re

def remove_non_alphanumeric_keep_vietnamese_extended(input):
    # Kiểm tra xem giá trị có phải là chuỗi hay không
    if isinstance(input, str):
        # Loại bỏ emoji và ký tự không mong muốn, giữ lại chữ cái, số, và các ký tự tiếng Việt
        cleaned_text = re.sub(r'[^\w\sÀ-ÿ]', ' ', input)
        return cleaned_text
    else:
        # Trả về giá trị gốc nếu không phải là chuỗi
        return input

# Đọc file CSV
df = pd.read_excel('D:/Github/e_commerce/Review.xlsx')

# Lấy tên cột đầu tiên
column_name = df.columns[0]

# Áp dụng hàm loại bỏ ký tự không mong muốn cho mỗi dòng trong cột
df[column_name] = df[column_name].apply(remove_non_alphanumeric_keep_vietnamese_extended)

# Xuất dữ liệu sau khi xử lý ra file CSV mới
df.to_excel('D:/Github/e_commerce/data_negative.xlsx', index=False)

print("Xử lý và xuất dữ liệu thành công.")

import pandas as pd

# # Đọc file Excel
# df = pd.read_excel('D:/Github/e_commerce/output_processed1.xlsx')
#
# # Tạo cột 'Sentiment' với nhãn 'Positive' cho tất cả các dòng
# df['Sentiment'] = 'Positive'
#
# # In dữ liệu mới có cột 'Sentiment'
# print(df)
#
# # Lưu dữ liệu mới ra file Excel
# df.to_excel('D:/Github/e_commerce/data.xlsx', index=False)


