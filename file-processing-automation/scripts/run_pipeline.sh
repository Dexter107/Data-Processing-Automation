#!/bin/bash
set -e

TODAY=$(date +%Y-%m-%d)

echo "▶ Starting pipeline ($TODAY)"
echo "📊 Checking for CSV files in data/input/"

# 1. Run Python FIRST (process + generate reports)
python3 scripts/process_csv.py

# 2. Then archive the processed CSV files
mkdir -p data/processed/$TODAY

if ls data/input/*.csv 1> /dev/null 2>&1; then
    echo "📦 CSV files found — archiving..."
    mv data/input/*.csv data/processed/$TODAY/
    echo "✔ CSV files archived in data/processed/$TODAY/"
else
    echo "⚠ No CSV files to archive"
fi

echo "✔ Pipeline completed successfully"
