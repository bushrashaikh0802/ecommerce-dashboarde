import pandas as pd
from dashboard.models import Sale

def run():
    df = pd.read_csv('C:\Users\HP\OneDrive\Desktop\e-commerce\ecommerce\Untitled spreadsheet - Sheet1.csv')  # Your dataset
    for _, row in df.iterrows():
        Sale.objects.create(
            order_id=row['Order ID'],
            customer_name=row['Customer Name'],
            product_category=row['Category'],
            product_name=row['Product'],
            quantity=row['Quantity'],
            price=row['Price'],
            order_date=row['Order Date']
        )
