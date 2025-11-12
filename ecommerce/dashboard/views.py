from django.shortcuts import render
from .models import Sale
import pandas as pd
import plotly.express as px

def dashboard_view(request):
    # Fetch all sales
    sales = Sale.objects.all().values()
    df = pd.DataFrame(sales)

    if df.empty:
        return render(request, 'dashboard/index.html', {'message': 'No data available yet.'})

    # Convert date column
    df['date'] = pd.to_datetime(df['date'])

    # --------- 🔹 Date Filter ----------
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    # --------- 🔹 KPI Calculations ----------
    total_revenue = df['total_amount'].sum()
    total_orders = len(df)
    unique_customers = df['customer_id'].nunique()
    avg_order_value = total_revenue / total_orders if total_orders else 0

    # --------- 🔹 Charts ----------
    top_categories = df.groupby('product_category')['total_amount'].sum().sort_values(ascending=False).head(5)
    monthly_sales = df.groupby(df['date'].dt.to_period('M'))['total_amount'].sum()

    fig1 = px.bar(
        top_categories, x=top_categories.index, y=top_categories.values,
        title='Top Categories by Revenue', labels={'x': 'Product Category', 'y': 'Total Revenue'}
    )

    fig2 = px.line(
        x=monthly_sales.index.astype(str), y=monthly_sales.values,
        title='Monthly Sales Trend', labels={'x': 'Month', 'y': 'Revenue'}
    )

    context = {
        'total_revenue': f"${total_revenue:,.2f}",
        'total_orders': total_orders,
        'unique_customers': unique_customers,
        'avg_order_value': f"${avg_order_value:,.2f}",
        'plot1': fig1.to_html(full_html=False),
        'plot2': fig2.to_html(full_html=False),
        'start_date': start_date or '',
        'end_date': end_date or '',
    }

    return render(request, 'dashboard/index.html', context)
