from datetime import datetime

from airflow.models import DAG
from airflow.providers.apache.spark.operators.spark_jdbc import SparkJDBCOperator
from airflow.providers.apache.spark.operators.spark_sql import SparkSqlOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

import os

with DAG(
    dag_id='spark_test',
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['FreeUni'],
) as dag:
    # [START howto_operator_spark_submit]
    submit_job = SparkSubmitOperator(
        application="/airflow/jobs/test_job.py", task_id="submit_job"
    )
    # [END howto_operator_spark_submit]

    submit_job_2 = SparkSubmitOperator(
        application=f"{os.getenv('SPARK_HOME')}/examples/src/main/python/pi.py", task_id="submit_job_2"
    )

    submit_job_3 = SparkSubmitOperator(
        application=f"/airflow/jobs/breaking_news.py", task_id="breaking_news"
    )

    [submit_job, submit_job_2] >> submit_job_3