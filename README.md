# Inventory Reconciler

A Python tool that compares system inventory against physical counts, calculates unit and dollar variances, and classifies discrepancies by severity. Built as a practical entry-level IT portfolio project demonstrating data processing, reporting, and retail operations knowledge.

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

Note: date folder will be empty, you will fill the folder based off running the script

## Setup (Run in Order)

```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate it (Windows PowerShell)
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate sample data
python sample_data_generator.py

# 5. Run the program
python main.py

# 6. (Optional) Launch web dashboard
streamlit run app.py
