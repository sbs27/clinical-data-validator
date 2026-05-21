"""Data quality metrics for clinical datasets."""

from typing import Dict, List, Any
import pandas as pd
import numpy as np


class DataQualityReporter:
    """Generate comprehensive data quality reports for clinical datasets."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the quality reporter with a DataFrame.
        
        Args:
            df: pandas DataFrame containing clinical observations
        """
        self.df = df
    
    def completeness_report(self) -> Dict[str, float]:
        """
        Calculate completeness percentage for each column.
        
        Returns:
            Dictionary with column names and completeness percentages
        """
        return {
            col: (self.df[col].count() / len(self.df)) * 100
            for col in self.df.columns
        }
    
    def uniqueness_report(self) -> Dict[str, int]:
        """
        Count unique values in each column.
        
        Returns:
            Dictionary with column names and unique value counts
        """
        return {
            col: self.df[col].nunique()
            for col in self.df.columns
        }
    
    def outlier_summary(self, numerical_cols: List[str] = None) -> Dict[str, int]:
        """
        Count outliers using IQR (Interquartile Range) method.
        
        Args:
            numerical_cols: List of column names to check (auto-detects if None)
            
        Returns:
            Dictionary with column names and outlier counts
        """
        if numerical_cols is None:
            numerical_cols = self.df.select_dtypes(include=['number']).columns.tolist()
        
        outliers = {}
        for col in numerical_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            outliers[col] = len(self.df[(self.df[col] < lower) | (self.df[col] > upper)])
        
        return outliers
    
    def data_type_report(self) -> Dict[str, str]:
        """
        Report data types of each column.
        
        Returns:
            Dictionary with column names and data types
        """
        return {col: str(self.df[col].dtype) for col in self.df.columns}
    
    def missing_value_report(self) -> Dict[str, int]:
        """
        Count missing values in each column.
        
        Returns:
            Dictionary with column names and missing value counts
        """
        return {col: self.df[col].isnull().sum() for col in self.df.columns}
    
    def value_distribution(self, column: str) -> Dict[Any, int]:
        """
        Get value distribution for a specific column.
        
        Args:
            column: Column name to analyse
            
        Returns:
            Dictionary with values and their frequencies
        """
        return self.df[column].value_counts().to_dict()
    
    def full_report(self) -> Dict:
        """
        Generate complete quality report with all metrics.
        
        Returns:
            Comprehensive dictionary with all quality metrics
        """
        numerical_cols = self.df.select_dtypes(include=['number']).columns.tolist()
        
        return {
            "basic_info": {
                "row_count": len(self.df),
                "column_count": len(self.df.columns),
                "memory_usage_mb": round(self.df.memory_usage(deep=True).sum() / (1024 * 1024), 2)
            },
            "completeness": self.completeness_report(),
            "missing_values": self.missing_value_report(),
            "uniqueness": self.uniqueness_report(),
            "data_types": self.data_type_report(),
            "outliers": self.outlier_summary(numerical_cols) if numerical_cols else {},
            "duplicate_rows": self.df.duplicated().sum(),
            "duplicate_percentage": round((self.df.duplicated().sum() / len(self.df)) * 100, 2) if len(self.df) > 0 else 0
        }
    
    def print_report(self) -> None:
        """Print a human-readable quality report."""
        report = self.full_report()
        
        print("\n" + "="*60)
        print("DATA QUALITY REPORT")
        print("="*60)
        
        print(f"\n BASIC INFO:")
        print(f"   • Total rows: {report['basic_info']['row_count']}")
        print(f"   • Total columns: {report['basic_info']['column_count']}")
        print(f"   • Memory usage: {report['basic_info']['memory_usage_mb']} MB")
        
        print(f"\n COMPLETENESS (top 5):")
        for col, pct in list(report['completeness'].items())[:5]:
            print(f"   • {col}: {pct:.1f}%")
        
        print(f"\n⚠️ MISSING VALUES:")
        missing_with_values = {k: v for k, v in report['missing_values'].items() if v > 0}
        if missing_with_values:
            for col, count in list(missing_with_values.items())[:5]:
                print(f"   • {col}: {count} missing")
        else:
            print(f"   • No missing values found!")
        
        print(f"\n DUPLICATES:")
        print(f"   • Duplicate rows: {report['duplicate_rows']} ({report['duplicate_percentage']}%)")
        
        print(f"\n OUTLIERS:")
        if report['outliers']:
            for col, count in report['outliers'].items():
                if count > 0:
                    print(f"   • {col}: {count} outliers")
        else:
            print(f"   • No outliers detected")
        
        print("="*60 + "\n")
