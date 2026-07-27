# Inventory Reconciler

A Python tool that compares system inventory against physical counts, calculates unit and dollar variances, and classifies discrepancies by severity. Built as a practical entry-level IT portfolio project demonstrating data processing, reporting, and retail operations knowledge.

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
