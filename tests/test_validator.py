"""Unit tests for clinical data validator."""

import pytest
from src.validator import ClinicalDataValidator, ValidationResult


class TestClinicalDataValidator:
    
    @pytest.fixture
    def validator(self):
        return ClinicalDataValidator()
    
    def test_valid_heart_rate(self, validator):
        """Test that normal heart rate passes validation."""
        observation = {
            "patient_id": "P001",
            "timestamp": "2024-01-01",
            "measurement_type": "heart_rate_bpm",
            "value": 75
        }
        result = validator.validate_observation(observation)
        assert result.is_valid is True
        assert "Within normal range" in result.message
    
    def test_high_heart_rate_fails(self, validator):
        """Test that elevated heart rate fails validation."""
        observation = {
            "patient_id": "P001",
            "measurement_type": "heart_rate_bpm",
            "value": 150,
            "timestamp": "2024-01-01"
        }
        result = validator.validate_observation(observation)
        assert result.is_valid is False
        assert "Out of range" in result.message
    
    def test_low_heart_rate_fails(self, validator):
        """Test that low heart rate fails validation."""
        observation = {
            "patient_id": "P001",
            "measurement_type": "heart_rate_bpm",
            "value": 40,
            "timestamp": "2024-01-01"
        }
        result = validator.validate_observation(observation)
        assert result.is_valid is False
        assert "Out of range" in result.message
    
    def test_unknown_measurement_type(self, validator):
        """Test that unrecognised measurement types are rejected."""
        observation = {
            "patient_id": "P001",
            "measurement_type": "unknown_metric",
            "value": 42,
            "timestamp": "2024-01-01"
        }
        result = validator.validate_observation(observation)
        assert result.is_valid is False
        assert "Unknown measurement type" in result.message
    
    def test_non_numeric_value(self, validator):
        """Test that non-numeric values are rejected."""
        observation = {
            "patient_id": "P001",
            "measurement_type": "heart_rate_bpm",
            "value": "NOT_A_NUMBER",
            "timestamp": "2024-01-01"
        }
        result = validator.validate_observation(observation)
        assert result.is_valid is False
        assert "Non-numeric" in result.message
    
    def test_batch_validation_mixed(self, validator):
        """Test batch validation with mixed valid and invalid records."""
        observations = [
            {"patient_id": "P001", "measurement_type": "heart_rate_bpm", "value": 70, "timestamp": "2024-01-01"},
            {"patient_id": "P002", "measurement_type": "heart_rate_bpm", "value": 200, "timestamp": "2024-01-01"},
            {"patient_id": "P003", "measurement_type": "temperature_celsius", "value": 36.5, "timestamp": "2024-01-01"},
        ]
        
        valid, invalid = validator.validate_batch(observations)
        
        assert len(valid) == 2
        assert len(invalid) == 1
