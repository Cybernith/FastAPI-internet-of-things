# Base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

# Copy app source
COPY . /app

# Expose port
EXPOSE 8000

# Environment
ENV PYTHONUNBUFFERED=1
ENV ENV=prod

# Start FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
