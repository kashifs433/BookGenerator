FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Expose the port your app runs on (FastAPI default = 8000)
EXPOSE 1111 1112

CMD ["python", "main.py"]