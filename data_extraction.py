import boto3
import pandas as pd
import requests
import tabula

class DataExtractor(): 
  def read_rds_table(self, db_connector, table_name):
    engine = db_connector.init_db_engine()
    table_detail = pd.read_sql_table(f"{table_name}",engine)
    return table_detail
  
  def retrieve_pdf_data(self, pdf_link):
    try:
      card_df = tabula.read_pdf(pdf_link, stream=True, pages='all', output_format="dataframe")
      if not card_df or len(card_df) == 0:
          raise ValueError("No tables found in the provided PDF.")
      card_df = pd.concat(card_df, ignore_index=True)
      return card_df
     
    except Exception as e:
        print(f"Error while retrieving data from PDF: {e}")
        return None
    
  def list_number_of_stores(self, endpoint, headers):
    response = requests.get(endpoint, headers=headers)
    response = response.json()
    number_of_stores = response["number_stores"]
    return  number_of_stores
  
  def retrieve_stores_data(self, store_endpoint_base, store_numbers, headers):
    list_of_stores = []
    for number in range(store_numbers):
      store_endpoint = f"{store_endpoint_base}/{number}"
      response = requests.get(store_endpoint, headers=headers)
      response = response.json()
      list_of_stores.append(response)
    
    store_df = pd.DataFrame(list_of_stores)
    return store_df
  
  def extract_from_s3(self, object_key, path):
    s3 = boto3.client('s3')
    s3.download_file("data-handling-public", object_key, path)
    if "csv" in path:
      products_df = pd.read_csv(path) 
    else:
      products_df = pd.read_json(path) 
    return products_df


  





