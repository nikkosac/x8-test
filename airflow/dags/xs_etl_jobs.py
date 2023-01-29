"""
ETL pipeline to identify group of accounts playing at the same date. 
we group by LastLoginIP, and Account CreateDate
2022-11-04
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
    dag_id='run_XS_etl_jobs',
    schedule='30 * * * *', 
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=['etl'],
) as dag:
    @task(task_id="print_the_context")
    def print_context(ds=None, **kwargs):
        """Print the Airflow context and ds variable from the context."""
        pprint(kwargs)
        print(ds)
        return 'Whatever you return gets printed in the logs'

    run_this = print_context()

    @task.external_python(task_id="update_the_sql_folder", python=os.fspath(sys.executable))
    def do_update_sql_folder():
        import sys
        sys.path.append('/opt/airflow/src')
        from etl_update_sql_folder import update_sql_folder
        return update_sql_folder()

    update_sql_folder_task = do_update_sql_folder()

    @task.external_python(task_id="upload_to_the_neo4j", python=os.fspath(sys.executable))
    def do_upload_to_neo4j():
        import sys
        sys.path.append('/opt/airflow/src')
        from etl_upload_to_neo4j import upload_to_neo4j
        return upload_to_neo4j()

    upload_to_neo4j_task = do_upload_to_neo4j()

    @task.external_python(task_id="high_win_bet_ratio", python=os.fspath(sys.executable))
    def do_high_win_bet_ratio():
        import sys
        sys.path.append('/opt/airflow/src')
        from etl_high_win_bet_ratio import run_etl_high_win_bet_ratio
        return run_etl_high_win_bet_ratio()

    high_win_bet_ratio_task = do_high_win_bet_ratio()

    @task.external_python(task_id="high_win_streak", python=os.fspath(sys.executable))
    def do_high_win_streak():
        import sys
        sys.path.append('/opt/airflow/src')
        from etl_high_win_streak import run_etl_high_win_streak
        return run_etl_high_win_streak()

    high_win_streak_task = do_high_win_streak()

    @task.external_python(task_id="update_member", python=os.fspath(sys.executable))
    def do_update_member():
        import sys
        sys.path.append('/opt/airflow/src')
        from etl_update_member import run_etl_update_member
        return run_etl_update_member()

    update_member_task = do_update_member()


    @task.external_python(task_id="post_IpGrp_WinStreak", python=os.fspath(sys.executable))
    def do_post_IpGrp_WinStreak():
        import sys
        sys.path.append('/opt/airflow/src')
        from etl_post_IpGrp_WinStreak import run_post_IpGrp_WinStreak
        return run_post_IpGrp_WinStreak()

    post_IpGrp_WinStreak_task = do_post_IpGrp_WinStreak()


    @task.external_python(task_id="report_pachin", python=os.fspath(sys.executable))
    def do_report_pachin():
        import sys
        sys.path.append('/opt/airflow/src')
        from report_pachin import run_report_pachin
        return run_report_pachin()

    report_pachin_task = do_report_pachin()


    run_this \
        >> update_sql_folder_task \
        >> upload_to_neo4j_task \
        >> high_win_bet_ratio_task \
        >> high_win_streak_task \
        >> update_member_task \
        >> post_IpGrp_WinStreak_task \
        >> report_pachin_task
