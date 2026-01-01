import pandas as pd
import numpy as np
from datetime import datetime

# Load the merged dataset
merged_df = pd.read_csv('olist_merged.csv')

# Convert timestamp columns to datetime
timestamp_cols = ['order_purchase_timestamp', 'order_approved_at', 
                   'order_delivered_carrier_date', 'order_delivered_customer_date', 
                   'order_estimated_delivery_date', 'shipping_limit_date']

for col in timestamp_cols:
    if col in merged_df.columns:
        merged_df[col] = pd.to_datetime(merged_df[col], errors='coerce')

# ========== LEAD TIME CALCULATION ==========

# 1. Processing Time (Order approval - Purchase)
merged_df['processing_time_hours'] = (
    (merged_df['order_approved_at'] - merged_df['order_purchase_timestamp']).dt.total_seconds() / 3600
).round(2)

# 2. Shipping Time (Customer delivery - Carrier date)
merged_df['shipping_time_hours'] = (
    (merged_df['order_delivered_customer_date'] - merged_df['order_delivered_carrier_date']).dt.total_seconds() / 3600
).round(2)

# 3. Total Lead Time (Customer delivery - Purchase)
merged_df['total_lead_time_hours'] = (
    (merged_df['order_delivered_customer_date'] - merged_df['order_purchase_timestamp']).dt.total_seconds() / 3600
).round(2)

# 4. Seller Preparation Time (Shipping limit - Purchase)
merged_df['seller_prep_time_hours'] = (
    (merged_df['shipping_limit_date'] - merged_df['order_purchase_timestamp']).dt.total_seconds() / 3600
).round(2)

# 5. Delivery Delay (Actual delivery - Estimated delivery)
merged_df['delivery_delay_hours'] = (
    (merged_df['order_delivered_customer_date'] - merged_df['order_estimated_delivery_date']).dt.total_seconds() / 3600
).round(2)

# Convert hours to days for better readability
merged_df['total_lead_time_days'] = (merged_df['total_lead_time_hours'] / 24).round(2)
merged_df['shipping_time_days'] = (merged_df['shipping_time_hours'] / 24).round(2)
merged_df['delivery_delay_days'] = (merged_df['delivery_delay_hours'] / 24).round(2)

# ========== STATISTICS ==========

print("=" * 80)
print("LEAD TIME ANALYSIS")
print("=" * 80)

# Total Lead Time Statistics
print("\n[1] TOTAL LEAD TIME (Order Purchase → Customer Delivery)")
print(f"   Mean: {merged_df['total_lead_time_days'].mean():.2f} days")
print(f"   Median: {merged_df['total_lead_time_days'].median():.2f} days")
print(f"   Std Dev: {merged_df['total_lead_time_days'].std():.2f} days")
print(f"   Min: {merged_df['total_lead_time_days'].min():.2f} days")
print(f"   Max: {merged_df['total_lead_time_days'].max():.2f} days")
print(f"   25th percentile: {merged_df['total_lead_time_days'].quantile(0.25):.2f} days")
print(f"   75th percentile: {merged_df['total_lead_time_days'].quantile(0.75):.2f} days")

# Processing Time Statistics
print("\n[2] PROCESSING TIME (Order Purchase → Order Approved)")
print(f"   Mean: {merged_df['processing_time_hours'].mean():.2f} hours")
print(f"   Median: {merged_df['processing_time_hours'].median():.2f} hours")
print(f"   Std Dev: {merged_df['processing_time_hours'].std():.2f} hours")

# Shipping Time Statistics
print("\n[3] SHIPPING TIME (Carrier Receipt → Customer Delivery)")
print(f"   Mean: {merged_df['shipping_time_days'].mean():.2f} days")
print(f"   Median: {merged_df['shipping_time_days'].median():.2f} days")
print(f"   Std Dev: {merged_df['shipping_time_days'].std():.2f} days")

# Delivery Delay Statistics
print("\n[4] DELIVERY DELAY (Actual vs. Estimated)")
delay_positive = merged_df[merged_df['delivery_delay_days'] > 0]
delay_negative = merged_df[merged_df['delivery_delay_days'] < 0]
print(f"   Mean delay: {merged_df['delivery_delay_days'].mean():.2f} days")
print(f"   On-time delivery rate: {((merged_df['delivery_delay_days'] <= 0).sum() / len(merged_df) * 100):.2f}%")
print(f"   Late delivery count: {len(delay_positive)} ({(len(delay_positive)/len(merged_df)*100):.2f}%)")
print(f"   Early delivery count: {len(delay_negative)} ({(len(delay_negative)/len(merged_df)*100):.2f}%)")

# ========== GROUP ANALYSIS ==========

print("\n" + "=" * 80)
print("LEAD TIME BY ORDER STATUS")
print("=" * 80)
for status in merged_df['order_status'].unique():
    status_data = merged_df[merged_df['order_status'] == status]
    print(f"\n{status.upper()}")
    print(f"   Count: {len(status_data)}")
    print(f"   Avg Lead Time: {status_data['total_lead_time_days'].mean():.2f} days")

# ========== REGIONAL ANALYSIS (TOP 10 STATES) ==========
print("\n" + "=" * 80)
print("LEAD TIME BY CUSTOMER STATE (TOP 10)")
print("=" * 80)
state_analysis = merged_df.groupby('customer_state').agg({
    'total_lead_time_days': ['mean', 'median', 'count'],
    'delivery_delay_days': 'mean'
}).round(2)
state_analysis.columns = ['Avg Lead Time (days)', 'Median Lead Time (days)', 'Count', 'Avg Delay (days)']
state_analysis = state_analysis.sort_values('Count', ascending=False).head(10)
print(state_analysis)

# ========== PRODUCT CATEGORY ANALYSIS (TOP 10) ==========
print("\n" + "=" * 80)
print("LEAD TIME BY PRODUCT CATEGORY (TOP 10)")
print("=" * 80)
category_analysis = merged_df.groupby('product_category_name_english').agg({
    'total_lead_time_days': ['mean', 'median', 'count'],
    'delivery_delay_days': 'mean'
}).round(2)
category_analysis.columns = ['Avg Lead Time (days)', 'Median Lead Time (days)', 'Count', 'Avg Delay (days)']
category_analysis = category_analysis.sort_values('Count', ascending=False).head(10)
print(category_analysis)

# ========== SELLER ANALYSIS (TOP 10 BY ORDER COUNT) ==========
print("\n" + "=" * 80)
print("LEAD TIME BY SELLER (TOP 10)")
print("=" * 80)
seller_analysis = merged_df.groupby('seller_id').agg({
    'total_lead_time_days': ['mean', 'median', 'count'],
    'delivery_delay_days': 'mean'
}).round(2)
seller_analysis.columns = ['Avg Lead Time (days)', 'Median Lead Time (days)', 'Count', 'Avg Delay (days)']
seller_analysis = seller_analysis.sort_values('Count', ascending=False).head(10)
print(seller_analysis)

# ========== SAVE ENHANCED DATASET ==========
output_file = 'olist_merged_with_leadtime.csv'
merged_df.to_csv(output_file, index=False)
print(f"\n✓ Enhanced dataset saved to: {output_file}")
print(f"  Columns added:")
print(f"    - processing_time_hours")
print(f"    - shipping_time_hours")
print(f"    - total_lead_time_hours")
print(f"    - seller_prep_time_hours")
print(f"    - delivery_delay_hours")
print(f"    - total_lead_time_days")
print(f"    - shipping_time_days")
print(f"    - delivery_delay_days")
