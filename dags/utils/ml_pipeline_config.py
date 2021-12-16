params = {
    "db_engine": "postgresql+psycopg2://airflow:airflow@postgres/airflow",
    "db_schema": "public",
    "db_experiments_table": "experiments",
    "db_batch_table": "batch_data",
    "test_split_ratio": 0.3,
    "cv_folds": 3,
    "max_pca_components": 30,
    "logreg_maxiter": 1000
}   