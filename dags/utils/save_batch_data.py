import pandas as pd
from sqlalchemy import create_engine

from utils.files_util import load_files
import utils.ml_pipeline_config as config

db_engine = config.params["db_engine"]
db_schema = config.params["db_schema"]
table_batch = config.params["db_batch_table"] 

def save_batch_data():
    df = load_files(['df'])[0]
    engine = create_engine(db_engine)
    df.to_sql(table_batch, engine, schema=db_schema, if_exists='replace', index=False)