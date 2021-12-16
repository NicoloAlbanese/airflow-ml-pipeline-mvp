import pandas as pd
from sqlalchemy import create_engine

from utils.files_util import load_files
import utils.ml_pipeline_config as config

db_engine = config.params["db_engine"]
db_schema = config.params["db_schema"]
table_name = config.params["db_experiments_table"] 

def track_experiments_info():
    df = load_files(['exp_info'])[0]
    engine = create_engine(db_engine)
    df.to_sql(table_name, engine, schema=db_schema, if_exists='append', index=False)
