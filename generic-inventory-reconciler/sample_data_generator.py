import pandas as pd
import random
from pathlib import Path
from datetime import datetime, timedelta

random.seed(42)
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

PRODUCTS = [
    ("SKU-10001", "Whole Milk 1 Gallon", "Dairy", 3.49),
    ("SKU-10002", "2% Milk 1 Gallon", "Dairy", 3.29),
    ("SKU-10003", "Large Eggs (12ct)", "Dairy", 2.99),
    ("SKU-10004", "Salted Butter 1lb", "Dairy", 4.49),
    ("SKU-10005", "Shredded Cheddar 8oz", "Dairy", 2.79),
    ("SKU-10006", "Greek Yogurt Plain 32oz", "Dairy", 5.49),
    ("SKU-10007", "Cream Cheese 8oz", "Dairy", 2.49),
    ("SKU-20001", "Bananas (per lb)", "Produce", 0.59),
    ("SKU-20002", "Red Apples (per lb)", "Produce", 1.49),
    ("SKU-20003", "Avocados (each)", "Produce", 1.29),
    ("SKU-20004", "Roma Tomatoes (per lb)", "Produce", 1.79),
    ("SKU-20005", "Iceberg Lettuce (head)", "Produce", 1.99),
    ("SKU-20006", "Yellow Onions (per lb)", "Produce", 0.89),
    ("SKU-20007", "Russet Potatoes (5lb bag)", "Produce", 3.99),
    ("SKU-30001", "Ground Beef 80/20 (per lb)", "Meat", 4.99),
    ("SKU-30002", "Chicken Breast Boneless (per lb)", "Meat", 3.79),
    ("SKU-30003", "Bacon 12oz", "Meat", 5.49),
    ("SKU-30004", "Pork Chops (per lb)", "Meat", 3.29),
    ("SKU-30005", "Italian Sausage (per lb)", "Meat", 4.29),
    ("SKU-40001", "White Bread Loaf", "Bakery", 2.49),
    ("SKU-40002", "Wheat Bread Loaf", "Bakery", 2.79),
    ("SKU-40003", "Flour Tortillas (10ct)", "Bakery", 2.99),
    ("SKU-40004", "Everything Bagels (6ct)", "Bakery", 3.49),
    ("SKU-50001", "White Rice 5lb", "Pantry", 4.99),
    ("SKU-50002", "Spaghetti Pasta 16oz", "Pantry", 1.29),
    ("SKU-50003", "Black Beans 15oz can", "Pantry", 0.99),
    ("SKU-50004", "Canned Corn 15oz", "Pantry", 0.89),
    ("SKU-50005", "Peanut Butter 16oz", "Pantry", 3.49),
    ("SKU-50006", "Grape Jelly 18oz", "Pantry", 2.79),
    ("SKU-50007", "Vegetable Oil 48oz", "Pantry", 4.29),
    ("SKU-50008", "All-Purpose Flour 5lb", "Pantry", 2.99),
    ("SKU-60001", "Frozen Pizza Pepperoni", "Frozen", 4.99),
    ("SKU-60002", "Frozen Broccoli 12oz", "Frozen", 1.79),
    ("SKU-60003", "Ice Cream Vanilla 1.5qt", "Frozen", 5.49),
    ("SKU-60004", "Frozen French Fries 2lb", "Frozen", 3.29),
    ("SKU-70001", "Bottled Water 24pk", "Beverages", 4.99),
    ("SKU-70002", "Coca-Cola 12pk cans", "Beverages", 7.49),
    ("SKU-70003", "Orange Juice 64oz", "Beverages", 3.99),
    ("SKU-70004", "Sparkling Water 12pk", "Beverages", 5.29),
]

def generate_system_inventory():
    rows = []
    for sku, name, category, cost in PRODUCTS:
        if category == "Produce":
            qty = random.randint(40, 180)
        elif category == "Meat":
            qty = random.randint(25, 90)
        elif category == "Dairy":
            qty = random.randint(30, 120)
        else:
            qty = random.randint(20, 100)
        rows.append({
            "sku": sku,
            "product_name": name,
            "category": category,
            "unit_cost": cost,
            "system_qty": qty
        })
    return pd.DataFrame(rows)

def generate_physical_count(system_df):
    rows = []
    for _, row in system_df.iterrows():
        system_qty = row["system_qty"]
        roll = random.random()
        if roll < 0.70:
            variance = random.randint(-3, 3)
        elif roll < 0.90:
            variance = random.randint(-12, 8)
        else:
            variance = random.choice([-25, -18, -15, 15, 20, 30])
        physical_qty = max(0, system_qty + variance)
        rows.append({
            "sku": row["sku"],
            "physical_qty": physical_qty,
            "counted_by": random.choice(["A.Smith", "J.Reyes", "M.Patel", "T.Nguyen", "K.Johnson"]),
            "count_date": (datetime.now() - timedelta(hours=random.randint(1, 8))).strftime("%Y-%m-%d %H:%M")
        })
    return pd.DataFrame(rows)

def main():
    print("Generating sample data...")
    system_df = generate_system_inventory()
    physical_df = generate_physical_count(system_df)
    system_df.to_csv(DATA_DIR / "system_inventory.csv", index=False)
    physical_df.to_csv(DATA_DIR / "physical_count.csv", index=False)
    print("Created data/system_inventory.csv")
    print("Created data/physical_count.csv")

if __name__ == "__main__":
    main()
