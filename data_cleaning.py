import numpy as np
import pandas as pd
import re

class DataCleaning():
  def clean_user_data(self,user_data_df):
    user_df = user_data_df.replace("NULL", np.nan)
    user_df['join_date'] = pd.to_datetime(user_df['join_date'], errors='coerce',format = 'mixed')
    user_df = user_df.dropna()
    return user_df
  
  def clean_card_data(self, df):
    df = df.replace("NULL", np.nan)
    df['date_payment_confirmed'] = pd.to_datetime(df['date_payment_confirmed'], errors='coerce',format = 'mixed')
    df['card_number']= df['card_number'].drop_duplicates()
    df['card_number'] = pd.to_numeric(df['card_number'], errors='coerce')
    df= df.dropna(subset=['date_payment_confirmed'])
    return df
  
  def called_clean_store_data(self,store_df):
    store_df = store_df.replace("NULL", np.nan)
    store_df['opening_date'] = pd.to_datetime(store_df['opening_date'], errors='coerce',format = 'mixed')
    store_df["staff_numbers"] = store_df["staff_numbers"].str.strip()
    store_df['staff_numbers'] = store_df['staff_numbers'].str.replace(r'[^0-9]', '', regex=True)
    store_df = store_df.dropna(subset=['opening_date'])
    return store_df
  
  def clean_orders_data(self, order_df):
    order_df = order_df.drop(columns=['1', 'first_name','last_name','level_0'])
    return order_df
  
  def convert_product_weights(self, product_df):
    def clean_and_convert_weight(weight):
      try:
        # Remove whitespace and convert to lowercase
        weight = weight.strip().lower()

        # Handle multiplicative cases like '40 x 100g'
        if 'x' in weight:
            parts = weight.split('x')
            if len(parts) == 2:
                try:
                    multiplier = float(parts[0].strip())
                    unit_value = parts[1].strip()
                    return clean_and_convert_weight(f"{multiplier * float(unit_value.replace('g', '').replace('kg', '').replace('ml', ''))}{unit_value[-1]}")
                except ValueError:
                    return None

        # Extract numeric value and unit using regex
        match = re.match(r'([\d.]+)\s*([a-z]*)', weight)
        if match:
            value, unit = match.groups()
            value = float(value)

            # Convert based on unit
            if 'kg' in unit:
                return value
            elif 'g' in unit:
                return value / 1000
            elif 'ml' in unit:
                return value / 1000  # Assuming 1ml = 1g
            else:
                return None  # Invalid or unknown unit

        # Return None for invalid weights
        return None
      except Exception as e:
        print(f"Error processing weight '{weight}': {e}")
        return None
    product_df['weight'] = product_df['weight'].apply(clean_and_convert_weight)
    return product_df
  
  def clean_products_data(self, product_df):
     product_df = product_df.replace("NULL", np.nan)
     product_df = product_df.dropna(subset=["weight"])
     return product_df
  
  def clean_date_times(self,date_df):
     date_df = date_df.replace("NULL", np.nan)
     date_df["day"] = pd.to_numeric(date_df["day"],errors="coerce")
     date_df["month"] = pd.to_numeric(date_df["month"],errors="coerce")
     date_df["year"] = pd.to_numeric(date_df["year"],errors="coerce")
     date_df = date_df.dropna()
     return date_df













