# Gunakan base image Python
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Salin dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua kode ke dalam container
COPY . .

# Copy .env.example to .env
RUN cp .env.example .env

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port untuk FastAPI
EXPOSE 8000

# Jalankan aplikasi
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]