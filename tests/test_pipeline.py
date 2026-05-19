"""Unit tests for clinical data pipeline."""

import pytest
import pandas as pd
from pathlib import Path
import tempfile
from src.pipeline import ClinicalDataPipeline


class TestClinicalDataPipeline:
    
    @pytest.fixture
    def pipeline(self):
        return ClinicalDataPipeline()
    
    @pytest.fixture
    def sample_dataframe(self):
        return pd.DataFrame([
            {"patient_id": "P001", "timestamp": "2024-01-01", "measurement_type": "heart_rate_bpm", "value": 72},
            {"patient_id": "P002", "timestamp": "2024-01-01", "measurement_type": "heart_rate_bpm", "value": 180},
            {"patient_id": "P003", "timestamp": "2024-01-01", "measurement_type": "temperature_celsius", "value": 36.8},
        ])
    
    def test_load_csv_missing_file(self, pipeline):
        """Test that loading a missing file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            pipeline.load_csv("nonexistent.csv")
    
    def test_validate_returns_valid_and_invalid(self, pipeline, sample_dataframe):
        """Test that validate separates valid from invalid records."""
        valid_df, invalid_df = pipeline.validate(sample_dataframe)
        
        # 2 valid (72, 36.8), 1 invalid (180)
        assert len(valid_df) == 2
        assert len(invalid_df) == 1
    
    def test_save_clean_data_creates_file(self, pipeline, sample_dataframe):
        """Test that save_clean_data actually writes a file."""
        valid_df, _ = pipeline.validate(sample_dataframe)
        
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            tmp_path = tmp.name
        
        pipeline.save_clean_data(valid_df, tmp_path)
        
        assert Path(tmp_path).exists()
        
        # Cleanup
        Path(tmp_path).unlink()
    
    def test_generate_quality_report(self, pipeline, sample_dataframe):
        """Test that quality report is generated correctly."""
        pipeline.validate(sample_dataframe)
        report = pipeline.generate_quality_report()
        
        assert "total_invalid" in report
        assert "quality_score" in report
        assert report["total_invalid"] == 1
