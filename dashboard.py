#!/usr/bin/env python3
"""
Generate an HTML quality report dashboard for clinical data.

Usage:
    python dashboard.py
    python dashboard.py --input data/raw/sample_observations.csv
"""

import argparse
import webbrowser
import tempfile
import sys
from pathlib import Path
import pandas as pd
from src.pipeline import ClinicalDataPipeline
from src.quality_metrics import DataQualityReporter


def generate_dashboard(input_file=None):
    """
    Generate HTML dashboard from clinical data.
    
    Args:
        input_file: Path to CSV file (uses sample data if None)
    """
    pipeline = ClinicalDataPipeline()
    
    # Load data
    if input_file:
        print(f"Loading data from {input_file}...")
        df = pipeline.load_csv(input_file)
    else:
        print("Loading sample data...")
        df = pipeline.load_csv("data/raw/sample_observations.csv")
    
    # Run validation
    print("Validating data...")
    valid_df, invalid_df = pipeline.validate(df)
    quality_report = pipeline.generate_quality_report()
    quality_metrics = pipeline.generate_quality_metrics(df)
    
    # Prepare data for display
    valid_count = len(valid_df)
    invalid_count = len(invalid_df)
    total_count = len(df)
    quality_score = quality_report['quality_score']
    
    # Color based on quality score
    score_color = "#28a745" if quality_score >= 80 else "#ffc107" if quality_score >= 50 else "#dc3545"
    score_status = "Good" if quality_score >= 80 else "Fair" if quality_score >= 50 else "Poor"
    
    # Create HTML
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clinical Data Quality Dashboard | UCLH SAFEHR</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f0f4f8;
            color: #2c3e50;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        /* Header */
        .header {{
            background: linear-gradient(135deg, #005EB8 0%, #003d7a 100%);
            color: white;
            padding: 40px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 2em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            opacity: 0.9;
            font-size: 1.1em;
        }}
        
        .badge {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            margin-top: 10px;
        }}
        
        /* Metrics Grid */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .metric-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        
        .metric-value {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 15px 0;
        }}
        
        .metric-label {{
            color: #6c757d;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .metric-good {{ color: #28a745; }}
        .metric-warning {{ color: #ffc107; }}
        .metric-danger {{ color: #dc3545; }}
        
        /* Sections */
        .section {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        
        .section h2 {{
            color: #005EB8;
            border-bottom: 2px solid #e9ecef;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        
        /* Tables */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e9ecef;
        }}
        
        th {{
            background: #f8f9fa;
            font-weight: 600;
            color: #495057;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
        
        /* Alert boxes */
        .alert {{
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        
        .alert-success {{
            background: #d4edda;
            color: #155724;
            border-left: 4px solid #28a745;
        }}
        
        .alert-warning {{
            background: #fff3cd;
            color: #856404;
            border-left: 4px solid #ffc107;
        }}
        
        .alert-danger {{
            background: #f8d7da;
            color: #721c24;
            border-left: 4px solid #dc3545;
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: 20px;
            color: #6c757d;
            font-size: 0.85em;
            border-top: 1px solid #e9ecef;
            margin-top: 30px;
        }}
        
        @media (max-width: 768px) {{
            .metrics-grid {{
                grid-template-columns: 1fr;
            }}
            .container {{
                padding: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>Clinical Data Quality Dashboard</h1>
            <p>UCLH SAFEHR Platform | Data Quality Monitoring</p>
            <div class="badge">Synthetic Data | Demonstration Purpose</div>
        </div>
        
        <!-- Quality Score Alert -->
        <div class="alert alert-{('success' if quality_score >= 80 else 'warning' if quality_score >= 50 else 'danger')}">
            <strong>Quality Score: {quality_score}% ({score_status})</strong>
            <br>Overall data quality assessment based on validation rules and completeness.
        </div>
        
        <!-- Metrics Grid -->
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Total Records</div>
                <div class="metric-value metric-good">{total_count}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Valid Records</div>
                <div class="metric-value metric-good">{valid_count}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Invalid Records</div>
                <div class="metric-value metric-{'danger' if invalid_count > 0 else 'good'}">{invalid_count}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Pass Rate</div>
                <div class="metric-value metric-{'good' if (valid_count/total_count*100) >= 80 else 'warning'}">{valid_count/total_count*100:.1f}%</div>
            </div>
        </div>
        
        <!-- Data Preview -->
        <div class="section">
            <h2>Data Preview (First 10 rows)</h2>
            {df.head(10).to_html(classes='data-table', index=False)}
        </div>
        
        <!-- Invalid Records -->
        <div class="section">
            <h2>Invalid Records</h2>
            {invalid_df.to_html(classes='data-table', index=False) if not invalid_df.empty else '<div class="alert alert-success">No invalid records found. All data passed validation.</div>'}
        </div>
        
        <!-- Quality Metrics Details -->
        <div class="section">
            <h2>Quality Metrics Details</h2>
            <table>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Completeness</td>
                    <td>{quality_metrics['completeness']}</td>
                </tr>
                <tr>
                    <td>Missing Values</td>
                    <td>{quality_metrics['missing_values']}</td>
                </tr>
                <tr>
                    <td>Duplicate Rows</td>
                    <td>{quality_metrics['duplicate_rows']} ({quality_metrics['duplicate_percentage']}%)</td>
                </tr>
                <tr>
                    <td>Memory Usage</td>
                    <td>{quality_metrics['basic_info']['memory_usage_mb']} MB</td>
                </tr>
            </table>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p>Generated by Clinical Data Validator v1.0 | NHS Data Pipeline Demo</p>
            <p>Built for UCLH SAFEHR Senior Software Engineer application</p>
            <p>Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
    """
    
    # Save to project folder instead of temp file
    output_path = "dashboard_report.html"
    with open(output_path, 'w') as f:
        f.write(html)
    
    # Open in browser with macOS-specific handling
    import subprocess
    import platform
    
    if platform.system() == 'Darwin':  # macOS
        subprocess.run(['open', output_path])
    elif platform.system() == 'Windows':
        subprocess.run(['start', output_path], shell=True)
    else:  # Linux
        subprocess.run(['xdg-open', output_path])
    
    print(f"\nDashboard opened in your browser.")
    print(f"File saved at: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate clinical data quality dashboard")
    parser.add_argument("--input", "-i", help="Path to input CSV file")
    parser.add_argument("--output", "-o", help="Save HTML to file instead of opening")
    
    args = parser.parse_args()
    
    if args.output:
        # Save to file without opening browser
        temp_path = generate_dashboard(args.input)
        import shutil
        shutil.copy(temp_path, args.output)
        print(f"Dashboard saved to: {args.output}")
    else:
        generate_dashboard(args.input)


if __name__ == "__main__":
    main()
