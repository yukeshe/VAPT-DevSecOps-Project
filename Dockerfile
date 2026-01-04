FROM python:3.11-alpine

WORKDIR /app

# Create instance directory with proper permissions
RUN mkdir -p /app/instance && chmod 777 /app/instance

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app/app.py"]
