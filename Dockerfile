# 1. בסיס עם Python
FROM python:3.11-slim

# 2. קובץ עבודה
WORKDIR /app

# 3. העתק קבצי תלויות
COPY ./requirements.txt /app/requirements.txt

# 4. התקנת תלויות
RUN pip install --no-cache-dir -r requirements.txt

# 5. העתק כל הקוד לתוך המכולה
COPY . /app

# 6. פותח פורט
EXPOSE 8000

# 7. הפקודה להרצת השרת
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]