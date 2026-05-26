

```
           Clinical Data Validator
```

A production-ready data quality pipeline for validating clinical observations against medical reference ranges. Built to demonstrate software engineering best practices for healthcare data pipelines in NHS environments.

---

## Overview

This validator processes clinical observation data (heart rate, blood pressure, temperature, oxygen saturation, glucose, electrolytes, and more) and validates each measurement against established medical reference ranges. Records outside clinical thresholds are flagged for review, while valid data proceeds through the pipeline.

**This project demonstrates the core competencies required for Senior Software Engineer (Data & AI Enablement) roles in healthcare:**

| Competency | Demonstration |
|------------|---------------|
| Python (primary research language) | Full implementation with type hints, dataclasses, pandas |
| Clinical awareness | Reference ranges from NICE/AHA/BTS guidelines |
| Testing discipline | 10+ unit tests with pytest, covering edge cases |
| Containerisation | Dockerfile for reproducible execution |
| CI/CD | GitHub Actions automated testing on every push |
| Documentation | Comprehensive docstrings and this README |
| Defensive programming | Input validation, explicit error handling |
| Data quality metrics | Completeness, outliers, duplicates, missing values |
| Visualisation | HTML dashboard for quality reporting |

> **Note on data:** This is a demonstration project using synthetic data only. Real patient data is confidential and cannot be shared publicly. The architectural patterns, testing discipline, and engineering practices shown here are exactly what I apply to production healthcare data.

---

## Quick Start

### Local Setup

```bash
# Clone the repository
git clone https://github.com/sbs27/clinical-data-validator.git
cd clinical-data-validator

# Install dependencies
pip install -r requirements.txt

# Run the test suite
pytest tests/ -v

# Run the pipeline on sample data
python -c "
from src.pipeline import ClinicalDataPipeline
pipeline = ClinicalDataPipeline()
df = pipeline.load_csv('data/raw/sample_observations.csv')
valid, invalid = pipeline.validate(df)
print(f'Valid: {len(valid)}, Invalid: {len(invalid)}')
print(pipeline.generate_quality_report())
"
```

### Docker Setup

```bash
# Build the container
docker build -t clinical-validator .

# Run the container (automatically runs tests on build)
docker run clinical-validator
```

### Run the Dashboard

```bash
# Generate interactive HTML quality dashboard
python dashboard.py

# Or with custom data file
python dashboard.py --input data/raw/edge_cases.csv
```

### Expected Output

```
Valid: 5, Invalid: 3
{'total_invalid': 3, 'quality_score': 85, 'issues': {'Out of range': 3}}
```

---

## Sample Datasets Included

| File | Description |
|------|-------------|
| sample_observations.csv | Mixed valid/invalid clinical observations |
| valid_data.csv | All valid data (100% pass rate) |
| edge_cases.csv | Extreme values for testing boundaries |
| mixed_quality.csv | Balanced mix of good and bad data |
| missing_values.csv | Tests handling of incomplete records |

---

## Architecture

### Project Structure

```
clinical-data-validator/
├── .github/
│   └── workflows/
│       └── test.yml          # CI/CD: runs tests on every push
├── src/
│   ├── __init__.py
│   ├── validator.py          # Clinical validation rules
│   ├── pipeline.py           # ETL orchestration
│   └── quality_metrics.py    # Data quality metrics
├── tests/
│   ├── __init__.py
│   ├── test_validator.py     # Unit tests for validation
│   └── test_pipeline.py      # Unit tests for pipeline
├── data/
│   ├── raw/                  # Input data directory
│   └── processed/            # Clean output data directory
├── dashboard.py              # HTML dashboard generator
├── Dockerfile
├── requirements.txt
└── README.md
```

### Design Decisions

| Decision | Rationale |
|----------|-----------|
| Separation of Concerns | Each module has a single responsibility |
| Dataclasses for Results | Type-safe, structured validation output |
| Batch Processing | Efficient for NHS-scale data |
| Quality Scoring | Researchers can filter by threshold |
| Defensive Programming | Explicit validation and error handling |
| Test Coverage | Tests for valid, invalid, and edge cases |

---

## Clinical Reference Ranges

All reference ranges are derived from established clinical guidelines:

| Measurement | Normal Range | Clinical Source |
|-------------|--------------|-----------------|
| Heart rate | 60-100 bpm | American Heart Association |
| Systolic BP | 90-120 mmHg | NICE Guideline NG136 |
| Diastolic BP | 60-80 mmHg | NICE Guideline NG136 |
| Respiratory rate | 12-20 breaths/min | British Thoracic Society |
| Temperature | 36.1-37.2 C | NICE Guideline NG143 |
| Oxygen saturation | 95-100% | British Thoracic Society |
| Glucose | 4.0-7.8 mmol/L | NICE Guideline NG28 |
| Potassium | 3.5-5.0 mmol/L | UK Kidney Association |
| Sodium | 135-145 mmol/L | UK Kidney Association |
| Creatinine | 60-110 umol/L | NICE Guideline |
| Haemoglobin | 12-16 g/dL | British Society for Haematology |
| Platelets | 150-450 x10^9/L | British Society for Haematology |

> **Note:** In production, these ranges would be configurable and approved by clinical governance.

---

## Test Suite

```bash
pytest tests/ -v
```

| Test | What it verifies |
|------|------------------|
| test_valid_heart_rate | Normal values pass validation |
| test_high_heart_rate_fails | Elevated values are rejected |
| test_low_heart_rate_fails | Depressed values are rejected |
| test_unknown_measurement_type | Unrecognised metrics are rejected |
| test_non_numeric_value | String values are rejected |
| test_batch_validation_mixed | Batch processing works correctly |
| test_load_csv_missing_file | Graceful file handling |
| test_validate_returns_valid_and_invalid | Correct partitioning |
| test_save_clean_data_creates_file | Output files are written |
| test_generate_quality_report | Quality metrics calculated |

---

## Quality Metrics Available

The `DataQualityReporter` class provides:

| Metric | Description |
|--------|-------------|
| Completeness | Percentage of non-null values per column |
| Outliers | Values outside 1.5x IQR range |
| Duplicates | Duplicate row detection and percentage |
| Missing values | Count of nulls per column |
| Data types | Automatic type detection |
| Memory usage | DataFrame memory footprint |

Example usage:

```python
from src.pipeline import ClinicalDataPipeline

pipeline = ClinicalDataPipeline()
df = pipeline.load_csv("data/raw/sample_observations.csv")

# Get full quality report
metrics = pipeline.generate_quality_metrics(df)
print(metrics['completeness'])
print(metrics['outliers'])

# Print readable report
pipeline.print_quality_report(df)
```

---

## CI/CD Pipeline (GitHub Actions)

Every push or pull request to `main` triggers:

1. Checkout code
2. Set up Python 3.11
3. Install dependencies
4. Run all pytest tests
5. Report pass/fail status

**View results:** Repository -> Actions tab -> "Clinical Data Pipeline Tests"

---

## Usage Examples

### Basic Pipeline

```python
from src.pipeline import ClinicalDataPipeline

pipeline = ClinicalDataPipeline()
df = pipeline.load_csv("data/raw/observations.csv")
valid_df, invalid_report = pipeline.validate(df)
pipeline.save_clean_data(valid_df, "data/processed/clean.csv")
report = pipeline.generate_quality_report()
print(f"Quality score: {report['quality_score']}%")
```

### Adding a New Measurement Type

```python
# In validator.py, add to REFERENCE_RANGES:
REFERENCE_RANGES = {
    # ... existing ranges ...
    "respiratory_rate": (12, 20)
}
```

### Custom Quality Threshold

```python
valid_df, invalid_df = pipeline.validate(df)

if pipeline.generate_quality_report()['quality_score'] > 90:
    pipeline.save_clean_data(valid_df, "output.csv")
else:
    print("Quality threshold not met")
```

### Running the Dashboard

```bash
python dashboard.py
python dashboard.py --input data/raw/edge_cases.csv
python dashboard.py --output my_dashboard.html
```

---

## Extending for NHS Production

In a live SAFEHR environment, this pipeline would be extended with:

| Extension | Implementation |
|-----------|----------------|
| Pseudonymisation | Tokenisation before validation |
| Audit logging | Immutable store for all runs |
| Configurable ranges | Database with versioning |
| Multiple formats | HL7/FHIR/OMOP loaders |
| Quality API | REST endpoint for metrics |
| Orchestration | Apache Airflow |
| EPIC integration | Direct connection to UCLH's system |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| ModuleNotFoundError: No module named 'src' | Run from repository root or `export PYTHONPATH=.` |
| Tests fail on Docker build | Check requirements.txt matches local environment |
| CSV missing required columns | Required: patient_id, timestamp, measurement_type, value |
| Value out of range | Check measurement_type matches REFERENCE_RANGES keys |
| Dashboard doesn't open | Run `open dashboard_report.html` manually |

---

## Dependencies

```
pandas==1.5.3
numpy==1.23.5
pytest==7.4.0
pydantic==1.10.8
```

---

## Author

**Shrabana Shruti**
- MSc Artificial Intelligence, Queen Mary University of London
- BSc Computer Science with AI, University of Nottingham

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | May 2026 | Initial release |
| 1.1.0 | May 2026 | Added quality metrics module |
| 1.2.0 | May 2026 | Added HTML dashboard |
| 1.3.0 | May 2026 | Added 12+ measurements and sample datasets |

---

## License

MIT License - Free for educational and demonstration purposes.

---

## Links

- **Repository:** https://github.com/sbs27/clinical-data-validator


---

