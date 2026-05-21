"""Clinical data validation rules for patient observations."""

from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of a single validation check."""
    is_valid: bool
    message: str
    record_id: str
    field: str


class ClinicalDataValidator:
    """Validates clinical observation data against medical reference ranges."""
    
    # Reference ranges based on standard clinical guidelines
    REFERENCE_RANGES = {
    # Cardiovascular
    "heart_rate_bpm": (60, 100),
    "systolic_bp_mmhg": (90, 120),
    "diastolic_bp_mmhg": (60, 80),
    # Respiratory
    "respiratory_rate_breaths_per_min": (12, 20),
    "oxygen_saturation_percent": (95, 100),
    # Metabolic
    "temperature_celsius": (36.1, 37.2),
    "glucose_mmol_L": (4.0, 7.8),
    # Electrolytes
    "potassium_mmol_L": (3.5, 5.0),
    "sodium_mmol_L": (135, 145),
    # Renal
    "creatinine_umol_L": (60, 110),
    # Haematology
    "haemoglobin_g_dL": (12, 16),
    "platelets_10_9_L": (150, 450)
}
    
    def validate_observation(self, observation: Dict) -> ValidationResult:
        """
        Validate a single clinical observation.
        
        Args:
            observation: Dict with keys: patient_id, timestamp, measurement_type, value
            
        Returns:
            ValidationResult indicating if the value is within clinical range
        """
        measurement_type = observation.get("measurement_type")
        value = observation.get("value")
        patient_id = observation.get("patient_id", "unknown")
        
        if measurement_type not in self.REFERENCE_RANGES:
            return ValidationResult(
                is_valid=False,
                message=f"Unknown measurement type: {measurement_type}",
                record_id=patient_id,
                field=measurement_type
            )
        
        min_val, max_val = self.REFERENCE_RANGES[measurement_type]
        
        if not isinstance(value, (int, float)):
            return ValidationResult(
                is_valid=False,
                message=f"Non-numeric value: {value}",
                record_id=patient_id,
                field=measurement_type
            )
        
        if min_val <= value <= max_val:
            return ValidationResult(
                is_valid=True,
                message="Within normal range",
                record_id=patient_id,
                field=measurement_type
            )
        else:
            return ValidationResult(
                is_valid=False,
                message=f"Out of range: {value} (normal: {min_val}-{max_val})",
                record_id=patient_id,
                field=measurement_type
            )
    
    def validate_batch(self, observations: List[Dict]) -> Tuple[List[Dict], List[ValidationResult]]:
        """
        Validate a batch of observations.
        
        Args:
            observations: List of observation dictionaries
            
        Returns:
            Tuple of (valid_observations, invalid_results)
        """
        valid = []
        invalid = []
        
        for obs in observations:
            result = self.validate_observation(obs)
            if result.is_valid:
                valid.append(obs)
            else:
                invalid.append(result)
        
        return valid, invalid
