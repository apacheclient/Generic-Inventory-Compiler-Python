# Generic-Style Inventory Reconciler

A practical inventory reconciliation tool that compares **system inventory** against **physical counts**.

This project demonstrates real-world retail operations knowledge combined with clean Python data processing. It is designed as an entry-level IT / systems portfolio project.

## Features

- Compare system vs physical inventory
- Calculate unit variance and dollar impact
- Automatic severity classification (Critical / High / Medium / Low)
- Clean terminal reports with color-coded severity
- Optional web dashboard using Streamlit
- Export results to CSV or Excel
- Includes realistic grocery sample data


## How to Run

# ======================
# STEP 6 + STEP 7 (All Commands)
# ======================

# Go into your project folder
cd heb-inventory-reconciler

# Create virtual environment
python -m venv .venv

# Activate virtual environment (PowerShell)
.venv\Scripts\activate

# Install required packages
pip install -r requirements.txt

# Generate the sample CSV data
python sample_data_generator.py

# Run the terminal version
python main.py

# Run the web dashboard (optional)
streamlit run app.py

# ======================
# Push to GitHub
# ======================

git init
git add .
git commit -m "Initial commit: HEB-style inventory reconciler"
git branch -M main
git remote add origin https://github.com/apacheclient/heb-inventory-reconciler.git
git push -u origin main