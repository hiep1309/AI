# Sử dụng Python làm base image
FROM python:3.12

# Đặt thư mục làm việc
WORKDIR /app

# Sao chép toàn bộ code vào container
COPY . .

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Mở cổng 5000
EXPOSE 5000

# Chạy ứng dụng Flask
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]

