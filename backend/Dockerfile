FROM python:3.13-slim

WORKDIR /app

# Copy requirements from root directory
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/app ./backend/app

# Set PYTHONPATH so Python can find the backend module
ENV PYTHONPATH=/app

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
