"""
Daily utility jobs, like syncing tables accross DB
2022-11-22
"""
from __future__ import annotations

import logging
import os
import shutil
import sys
import tempfile
import time
from pprint import pprint

import pendulum

from airflow import DAG
from airflow.decorators import task

log = logging.getLogger(__name__)

PYTHON = sys.executable

BASE_DIR = tempfile.gettempdir()

with DAG(
    dag_id='run_XS_etl_daily',
    schedule='50 0 * * *', 
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=['etl'],
) as dag:
    @task(task_id="print_the_context")
    def print_context(ds=None, **kwargs):
        """Daily task to sync tables across DB."""
        pprint(kwargs)
        print(ds)
        return 'Whatever you return gets printed in the logs'

    run_this = print_context()

    @task.external_python(task_id="daily_db_sync", python=os.fspath(sys.executable))
    def do_daily_db_sync():
        import sys
        sys.path.append('/opt/airflow/src')
        from etl_daily_db_sync import run_daily_db_sync
        return run_daily_db_sync()

    daily_db_sync_task = do_daily_db_sync()

    run_this \
        >> daily_db_sync_task
