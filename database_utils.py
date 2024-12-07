import yaml
from sqlalchemy import create_engine, inspect

class DatabaseConnector():
  def read_db_creds(self):
    with open("db_creds.yaml","r") as creds_file:
      creds = yaml.safe_load(creds_file)
    return creds
  
  def init_db_engine(self):
    creds = self.read_db_creds()
    user = creds["RDS_USER"]
    password = creds["RDS_PASSWORD"]
    host = creds["RDS_HOST"]
    port = creds["RDS_PORT"]
    db = creds["RDS_DATABASE"]
    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}")
    return engine
  
# psycopg2 and SQLAlchemy
  def list_db_tables(self):
    engine = self.init_db_engine()
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return tables

  def upload_to_db(self,dataframe,table_name):
    engine = create_engine(f"postgresql+psycopg2://postgres:baobeiying123@localhost:5433/sales_data")
    dataframe.to_sql(f"{table_name}",engine,if_exists='replace')