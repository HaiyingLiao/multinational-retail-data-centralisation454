import yaml
from sqlalchemy import create_engine, inspect

class DatabaseConnector():
  def read_db_creds(self, yaml_file):
    with open(yaml_file,"r") as creds_file:
      creds = yaml.safe_load(creds_file)
    return creds
  
  def init_db_engine(self):
    creds = self.read_db_creds("db_creds.yaml")
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
    creds = self.read_db_creds("pgadmin4_creds.yaml")
    user = creds["USER"]
    password = creds["PASSWORD"]
    host = creds["HOST"]
    port = creds["PORT"]
    db = creds["DATABASE"]
    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}")
    dataframe.to_sql(f"{table_name}",engine,if_exists='replace')