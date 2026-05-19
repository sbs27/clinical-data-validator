```
 Clinical Data Validator
```
A production-ready data quality pipeline for validating clinical observations against medical reference ranges. Built to demonstrate software engineering best practices for healthcare data pipelines in NHS environments.

---

###  Overview

This validator processes clinical observation data (heart rate, blood pressure, temperature, oxygen saturation) and validates each measurement against established medical reference ranges. Records outside clinical thresholds are flagged for review, while valid data proceeds through the pipeline.

**This project demonstrates the core competencies required for Senior Software Engineer (Data & AI Enablement) roles in healthcare:**

| Competency | Demonstration |
|------------|---------------|
| Python (primary research language) | Full implementation with type hints, dataclasses, pandas |
| Clinical awareness | Reference ranges from NICE/AHA/BTS guidelines |
| Testing discipline | 7+ unit tests with pytest, covering edge cases |
| Containerisation | Dockerfile for reproducible execution |
| CI/CD | GitHub Actions automated testing on every push |
| Documentation | Comprehensive docstrings and this README |
| Defensive programming | Input validation, explicit error handling |

---

##  Quick Start

### Local Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/clinical-data-validator.git
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

### Expected Output

```
Valid: 5, Invalid: 3
{'total_invalid': 3, 'quality_score': 85, 'issues': {'Out of range': 3}}
```

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
│   ├── validator.py          # Clinical validation rules & reference ranges
│   └── pipeline.py           # ETL orchestration & data quality reporting
├── tests/
│   ├── __init__.py
│   ├── test_validator.py     # Unit tests for validation logic
│   └── test_pipeline.py      # Unit tests for ETL pipeline
├── data/
│   ├── raw/                  # Input data directory
│   │   └── sample_observations.csv
│   └── processed/            # Clean output data directory
├── Dockerfile                # Container configuration
├── requirements.txt          # Python dependencies
├── .gitignore                # Exclude cache, env files, data
└── README.md                 # This file
```

### Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Separation of Concerns** | `validator.py` contains only validation rules; `pipeline.py` handles orchestration. Easy to add new measurement types without touching pipeline logic. |
| **Dataclasses for Results** | `ValidationResult` provides structured, type-safe validation output. |
| **Batch Processing** | `validate_batch()` processes multiple records efficiently, suitable for NHS-scale data. |
| **Quality Scoring** | Each dataset receives a quality score (0-100). Researchers can filter by threshold. |
| **Defensive Programming** | Every public method validates inputs and raises explicit exceptions. |
| **Test Coverage** | Tests for valid data, invalid data, edge cases, and missing files. |

---

##  Clinical Reference Ranges

All reference ranges are derived from established clinical guidelines:

| Measurement | Normal Range | Clinical Source |
|-------------|--------------|-----------------|
| Heart rate | 60-100 bpm | American Heart Association (AHA) |
| Systolic BP | 90-120 mmHg | NICE Guideline NG136 |
| Diastolic BP | 60-80 mmHg | NICE Guideline NG136 |
| Temperature | 36.1-37.2°C | NICE Guideline NG143 |
| Oxygen saturation | 95-100% | British Thoracic Society |

> **Note:** In a production NHS environment, these ranges would be configurable via a reference data table and approved by clinical governance.

---

##  Test Suite

```bash
pytest tests/ -v
```

**Test coverage includes:**

| Test | What it verifies |
|------|------------------|
| `test_valid_heart_rate` | Normal values pass validation |
| `test_high_heart_rate_fails` | Elevated values are rejected |
| `test_low_heart_rate_fails` | Depressed values are rejected |
| `test_unknown_measurement_type` | Unrecognised metrics are rejected |
| `test_non_numeric_value` | String values in numeric fields are rejected |
| `test_batch_validation_mixed` | Batch processing correctly separates valid/invalid |
| `test_load_csv_missing_file` | Graceful handling of missing files |
| `test_validate_returns_valid_and_invalid` | Correct partitioning of results |
| `test_save_clean_data_creates_file` | Output files are written correctly |
| `test_generate_quality_report` | Quality metrics are calculated accurately |

---

##  CI/CD Pipeline (GitHub Actions)

Every push or pull request to `main` triggers:

```yaml
1. Checkout code
2. Set up Python 3.11
3. Install dependencies
4. Run all pytest tests
5. Report pass/fail status
```

**View results:** Repository → Actions tab → "Clinical Data Pipeline Tests"

---

##  Usage Examples

### Basic Pipeline

```python
from src.pipeline import ClinicalDataPipeline

pipeline = ClinicalDataPipeline()

# Load data
df = pipeline.load_csv("data/raw/observations.csv")

# Validate against clinical ranges
valid_df, invalid_report = pipeline.validate(df)

# Save clean data for research use
pipeline.save_clean_data(valid_df, "data/processed/clean_observations.csv")

# Generate quality report
report = pipeline.generate_quality_report()
print(f"Data quality score: {report['quality_score']}%")
```

### Adding a New Measurement Type

```python
# In validator.py, add to REFERENCE_RANGES:
REFERENCE_RANGES = {
    # ... existing ranges ...
    "respiratory_rate_breaths_per_minute": (12, 20)
}
```

### Custom Quality Threshold

```python
valid_df, invalid_df = pipeline.validate(df)

# Only accept records with quality score > 90%
if pipeline.generate_quality_report()['quality_score'] > 90:
    pipeline.save_clean_data(valid_df, "output.csv")
else:
    print("Quality threshold not met - investigate data source")
```

---

##  Extending for NHS Production

In a live SAFEHR environment, this pipeline would be extended with:

| Extension | Implementation |
|-----------|----------------|
| **Pseudonymisation** | Add tokenisation step before validation |
| **Audit logging** | Log every validation run to immutable store |
| **Configurable ranges** | Store reference ranges in database with versioning |
| **Multiple source formats** | Add loaders for HL7/FHIR/OMOP |
| **Quality dashboard** | Expose metrics via REST API |
| **Airflow orchestration** | Schedule regular validation runs |


----


##  Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'src'` | Run from repository root directory, or `export PYTHONPATH=.` |
| Tests fail on Docker build | Check `requirements.txt` matches local environment |
| CSV missing required columns | Required: `patient_id`, `timestamp`, `measurement_type`, `value` |
| Value out of range despite being clinical | Check measurement_type string matches keys in `REFERENCE_RANGES` |

---

##  Dependencies

```
pandas==2.0.3    # Data manipulation
pytest==7.4.0    # Testing framework
pydantic==2.1.0  # Data validation (extensible)
```

---

##  Author

**Shrabana Shruti**
- MSc Artificial Intelligence, Queen Mary University of London
- BSc Computer Science with AI, University of Nottingham

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | May 2026 | Initial release: validator, pipeline, tests, CI/CD, Docker |

---

##  License

MIT License - Free for educational and demonstration purposes.

---

##  Links

- **Repository:** `https://github.com/sbs27/clinical-data-validator`


---

*This project was prepared as part of the application for Senior Software Engineer (Data & AI Enablement) at University College London Hospitals NHS Foundation Trust.*

