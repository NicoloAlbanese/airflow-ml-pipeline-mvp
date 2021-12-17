# airflow-ml-pipeline-mvp

Machine Learning pipeline MVP on Docker and Apache Airflow

__Author__: Nicolò C. Albanese (nicolo_albanese@outlook.it)

![Pipeline](https://github.com/NicoloAlbanese/airflow-ml-pipeline-mvp/blob/main/img/pipeline.png)

## 1. Prerequisites

- Docker Compose

## 2. Setup 

### 2.1 Configuration file

Starting from the [Airflow's official Docker Compose yaml file](https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml), the following changes are applied:

1. Set the AIRFLOW__CORE__EXECUTOR to LocalExecutor to run the pipeline locally.
2. Remove the definitions of the Redis, Flower and Worker services and their dependencies, as they are not needed for a local execution. 
3. Set the AIRFLOW__CORE__LOAD_EXAMPLES to false, as we do not want to load the native examples when accessing the web UI.
4. Populate the \_PIP_ADDITIONAL_REQUIREMENTS with: ${\_PIP_ADDITIONAL_REQUIREMENTS:-scikit-learn}, as we make use of the scikit-learn library for this example.
5. Create two more Docker volumes, respectively:
   5.1 ./data:/opt/airflow/data, in order to store the data.
   5.2 ./models:/opt/airflow/models, in order to store the model objects.

### 2.2 Execution

From command line:

```
docker-compose -f docker-compose.yaml up -d
```

Airflow UI is accassible at _localhost:8080_ by web browser.

Saved models can be found either in the _models_ subfolder within the project or by:

```
docker container exec -it airflow-dev_airflow-scheduler_1 bash

cd /opt/airflow/models

ls -l
```

Experiment tracking table can be checked by:

```
docker container exec -it airflow-dev_airflow-scheduler_1 bash

import pandas as pd

from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://airflow:airflow@postgres/airflow')

pd.read_sql('SELECT * FROM experiments', engine)
```

## 3. DAG

Graph view:

![Graph](https://github.com/NicoloAlbanese/airflow-ml-pipeline-mvp/blob/main/img/pipelinechart.png)

Tree view:

![Tree](https://github.com/NicoloAlbanese/airflow-ml-pipeline-mvp/blob/main/img/treeview.png)

## 4. Caveats

1. Airflow is an orchestrator. Ideally, it should not perform the tasks, but simply wrapping them around a logical structure allowing scheduling, monitoring and scaling.
2. We made use of the Local Executor to achieve a working local environment for testing purposes. Nevertheless, in order to enable scaling and pushing tasks to worker nodes, other types of executors should be used instead, such as the Celery Executor or Kubernetes Executor.
3. We stored data in the native PostgreSQL natively available and associated with the Airflow's metastore. This allowed to create a working example without specifying further services. Nevertheless, separation of duties and life cycle decoupling would require to store pipeline's data externally to the orchestrator's components.
4. We installed the needed dependencies by leveraging the \_PIP_ADDITIONAL_REQUIREMENTS configuration property. Although convenient for testing purposes, it would not be recommended for production systems. [Custom images](https://airflow.apache.org/docs/docker-stack/build.html) should be built instead.
5. In a real world scenario involving large datasets, Python and Pandas (as well as csv files) would not be the most favourable approach towards data manipulation, whereas Spark is preferable.


## 5. References

https://nicolo-albanese.medium.com/end-to-end-machine-learning-pipeline-with-docker-and-apache-airflow-from-scratch-35f6a75f57ad
