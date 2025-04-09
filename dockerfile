FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
ENV TZ=Asia/Bangkok
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]

