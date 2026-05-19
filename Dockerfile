FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY tests/ ./tests/
COPY data/ ./data/

# Run tests on build
RUN pytest tests/ -v

CMD ["python", "-c", "from src.pipeline import ClinicalDataPipeline; print('Clinical Data Pipeline ready. Container running successfully.')"]
