import yaml
from data_extraction import DataExtractor
from data_cleaning import DataCleaning
from database_utils import DatabaseConnector

if __name__ == "__main__":
  extractor = DataExtractor()
  data_cleaner = DataCleaning()
  db_conn = DatabaseConnector()

# # user table:
# ## tables in database:
#   tables = db_conn.list_db_tables()
#   print("Tables in the database:", tables)
# ## Identify the user data table
#   user_data_table = [table for table in tables if "users" in table][0]
#   print("User data table:", user_data_table)
# ## Extract user data into a DataFrame
#   user_data_df = extractor.read_rds_table(db_conn, user_data_table)
#   print(user_data_df.info())
# ## clean user table
#   cleaned_user_data = data_cleaner.clean_user_data(user_data_df)
#   print(cleaned_user_data.info())
# ## upload user data to database
#   db_conn.upload_to_db(cleaned_user_data, "dim_users")

#################################################################################
# # card data: 
# # extract card data
#   card_df = extractor.retrieve_pdf_data("card_details.pdf")
#   print(card_df.info())
#   cleaned_card_df = data_cleaner.clean_card_data(card_df)
#   print(cleaned_card_df.info())
# ## upload user data to database
#   db_conn.upload_to_db(cleaned_card_df, "dim_card_details")

#################################################################################
# #store data:
# ## get total store numbers
#   with open("stores_creds.yaml","r") as creds_file:
#     stores_api_creds = yaml.safe_load(creds_file)
#     number_of_stores_endpoint = stores_api_creds["NUMBER_OF_STORES_ENDPOINT"]
#     header = stores_api_creds["HEADER"]
#     store_numbers = extractor.list_number_of_stores(number_of_stores_endpoint,header)
#     print(f"total stores: {store_numbers}")
# ## get store data:
#     store_endpoint_base = stores_api_creds["STORE_ENDPOINT_BASE"]
#     store_data = extractor.retrieve_stores_data(store_endpoint_base, store_numbers, header)
#     print(store_data.info())
# ## clean store data
#     cleaned_store_data = data_cleaner.called_clean_store_data(store_data)
#     print(cleaned_store_data.info())
# ## upload to database
#     db_conn.upload_to_db(cleaned_store_data, "dim_store_details")

#################################################################################
# # products data:
# ## extract products data
#   products_data = extractor.extract_from_s3("products.csv","products.csv")
#   print(products_data.info())
# ## convert product weights 
#   coverted_weights_product_data = data_cleaner.convert_product_weights(products_data)
# ## clean products data
#   cleaned_product_data = data_cleaner.clean_products_data(coverted_weights_product_data)
#   print(cleaned_product_data.info())
# ## upload to database
#   db_conn.upload_to_db(cleaned_product_data, "dim_products")

#################################################################################
# # order table
# ## extract order table
#   order_data = extractor.read_rds_table(db_conn, 'orders_table')
# ## clean order table
#   cleaned_order_data = data_cleaner.clean_orders_data(order_data)
#   print(cleaned_order_data.info())
# ## upload to database
#   db_conn.upload_to_db(cleaned_order_data, "orders_table")

#################################################################################
# # date times
# ## extract date time data:
#   date_time_data = extractor.extract_from_s3("date_details.json","date_details.json")
# ## clean date time data:
#   cleaned_date_time_data = data_cleaner.clean_date_times(date_time_data)
#   print(cleaned_date_time_data.info())
# ## upload to database
#   db_conn.upload_to_db(cleaned_date_time_data, "dim_date_times")

#################################################################################
# check max number for column :
#################################################################################
  # max_len = cleaned_product_data['product_code'].astype(str).str.len().max() 
  # print(max_len)

