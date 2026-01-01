
import pandas as pd
import glob

# Path to the data directory
path = r'ficb4/data/pj1/olist' # use your path
all_files = glob.glob(path + "/*.csv")

data = {}
for f in all_files:
    df_name = f.split('\\')[-1].replace('.csv', '')
    data[df_name] = pd.read_csv(f, encoding='utf-8')

# Merge orders and customers
merged_df = pd.merge(data['olist_orders_dataset'], data['olist_customers_dataset'], on='customer_id')

# Merge with order_items
merged_df = pd.merge(merged_df, data['olist_order_items_dataset'], on='order_id')

# Merge with order_payments
merged_df = pd.merge(merged_df, data['olist_order_payments_dataset'], on='order_id')

# Merge with order_reviews
merged_df = pd.merge(merged_df, data['olist_order_reviews_dataset'], on='order_id')

# Merge with products
merged_df = pd.merge(merged_df, data['olist_products_dataset'], on='product_id')

# Merge with sellers
merged_df = pd.merge(merged_df, data['olist_sellers_dataset'], on='seller_id')

# Merge with product_category_name_translation
merged_df = pd.merge(merged_df, data['product_category_name_translation'], on='product_category_name', how='left')

# Merge with geolocation
# Geolocation data has a different structure and might need a different merge strategy.
# For now, I will skip it as it's large and may not directly join.

# Save the merged dataframe
merged_df.to_csv('ficb4/data/pj1/olist/olist_merged.csv', index=False)

print("Merged file created successfully!")
print(merged_df.info())
