"""ETL pipeline for processing clinical data."""

import pandas as pd
from pathlib import Path
from typing import Tuple, Optional
from .validator import ClinicalDataValidator, ValidationResult


class ClinicalDataPipeline:
    """
    Clinical data ETL pipeline with built-in validation.
    
    Example:
        pipeline = ClinicalDataPipeline()
        df = pipeline.load_csv("data/raw/observations.csv")
        valid_df, report = pipeline.validate(df)
        pipeline.save_clean_data(valid_df, "data/processed/clean_observations.csv")
    """
    
    def __init__(self):
        self.validator = ClinicalDataValidator()
        self.validation_report = []
    
    def load_csv(self, filepath: str) -> pd.DataFrame:
        """
        Load clinical data from CSV.
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            DataFrame with clinical observations
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If required columns are missing
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        df = pd.read_csv(filepath)
        
        # Ensure required columns exist
        required_columns = {"patient_id", "timestamp", "measurement_type", "value"}
        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            raise ValueError(f"Missing required columns: {missing}")
        
        return df
    
    def validate(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Validate all observations in a DataFrame.
        
        Args:
            df: DataFrame with clinical observations
            
        Returns:
            Tuple of (valid_dataframe, invalid_report_dataframe)
        """
        observations = df.to_dict("records")
        valid_obs, invalid_results = self.validator.validate_batch(observations)
        
        valid_df = pd.DataFrame(valid_obs) if valid_obs else pd.DataFrame()
        
        invalid_report = pd.DataFrame([{
            "patient_id": r.record_id,
            "field": r.field,
            "issue": r.message
        } for r in invalid_results])
        
        self.validation_report = invalid_results
        
        return valid_df, invalid_report
    
    def save_clean_data(self, df: pd.DataFrame, output_path: str) -> None:
        """Save validated data to CSV."""
        if df.empty:
            print("Warning: No valid data to save")
            return
        
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False)
        print(f"Saved {len(df)} records to {output_path}")
    
    def generate_quality_report(self) -> dict:
        """Generate a data quality summary report."""
        total = len(self.validation_report)
        if total == 0:
            return {"total_invalid": 0, "quality_score": 100.0}
        
        # Group issues by type
        issues = {}
        for result in self.validation_report:
            issue_type = result.message.split(":")[0] if ":" in result.message else result.message
            issues[issue_type] = issues.get(issue_type, 0) + 1
        
        return {
            "total_invalid": total,
            "quality_score": max(0, 100 - (total * 5)),
            "issues": issues
        }
