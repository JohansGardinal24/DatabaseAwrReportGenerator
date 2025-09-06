# Oracle AWR Report Generator

A Python tool for generating Oracle Automatic Workload Repository (AWR) reports with an interactive command-line interface.

## 📋 Description

This tool connects to an Oracle database and generates AWR reports by querying historical performance data. It provides a user-friendly interface to select snapshot ranges and customize report parameters.

## ✨ Features

- **Interactive CLI**: User-friendly prompts for all parameters
- **Snapshot Selection**: Displays available snapshots with timestamps
- **Flexible Date Range**: Generate reports for 1-30 days of historical data
- **HTML Report Output**: Generates comprehensive AWR reports in HTML format
- **Input Validation**: Robust error handling and input validation
- **Custom Report Names**: Option to specify custom filenames with validation

## 🔧 Prerequisites

- Python 3.7+
- Oracle Database 11g or higher
- Oracle Client libraries installed
- Required Python packages:
  ```bash
  pip install oracledb
