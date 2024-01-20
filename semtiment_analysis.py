import pandas as pd

# Đọc file CSV
positive_df = pd.read_excel('D:/Github/e_commerce/data_positive.xlsx')
negative_df = pd.read_excel('D:/Github/e_commerce/data_negative.xlsx')
positive_df_subset = positive_df.head(1500) #Cắt ra 1000 nghìn dòng cho cân đối

# Ghép nối hai bảng dữ liệu
merged_df = pd.concat([positive_df_subset, negative_df], ignore_index=True)

#Làm sạch dữ liệu
#B1: Chuyển đổi văn bản thành chữ thường
merged_df['Reviews'] = merged_df['Reviews'].str.lower()

#B2: Loại bỏ dấu câu
import string
def remove_punctuation(text):
    if isinstance(text, str):
        return text.translate(str.maketrans('', '', string.punctuation))
    return str(text)

merged_df['Reviews'] = merged_df['Reviews'].apply(remove_punctuation)

#B3: Loại bỏ stopwords
from stop_words import get_stop_words
stop_words = get_stop_words('vi')
merged_df['Reviews'] = merged_df['Reviews'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))

#B4: Token
from underthesea import word_tokenize
merged_df['Reviews'] = merged_df['Reviews'].apply(word_tokenize)

#---------------- Chia dữ liệu tập huấn
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(merged_df['Reviews'], merged_df['Sentiment'], test_size=0.2, random_state=42)
#----------------Xây dựng mô hình Sentiment Analysis
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Sử dụng CountVectorizer để chuyển đổi văn bản thành ma trận đặc trưng
vectorizer = CountVectorizer()
X_train_str = [' '.join(tokens) for tokens in X_train]
X_test_str = [' '.join(tokens) for tokens in X_test]
X_train_vectorized = vectorizer.fit_transform(X_train_str)
X_test_vectorized = vectorizer.transform(X_test_str)


# Đoạn văn bản bạn muốn kiểm thử
text_to_test = "sản phẩm 10 điểm"

# Tiến hành các bước làm sạch dữ liệu
text_to_test = text_to_test.lower()
text_to_test = remove_punctuation(text_to_test)
text_to_test = ' '.join([word for word in text_to_test.split() if word not in stop_words])
text_to_test_tokens = word_tokenize(text_to_test)
text_to_test_str = ' '.join(text_to_test_tokens)
text_to_test_vectorized = vectorizer.transform([text_to_test_str])



# Huấn luyện mô hình Logistic Regression
model = LogisticRegression(random_state=42)
model.fit(X_train_vectorized, y_train)
# Đánh giá mô hình trên tập kiểm tra
y_pred = model.predict(X_test_vectorized)


accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')
print(classification_report(y_test, y_pred))
prediction = model.predict(text_to_test_vectorized)
print(f"Đoạn văn bản được dự đoán là: {prediction[0]}")













