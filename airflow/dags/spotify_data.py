import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime, timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
import sqlite3
import logging

DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
USER_ID = "andres.wv"
CLIENT_ID = "e32a43c67dd04bb49f9b13d880b999a3"
CLIENT_SECRET = "8aa8490b77e846c098cccb0586b86ca1"
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='spotify_data',
    default_args=default_args,
    description='Extract info from Spotify API and store it in a SQLite database',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['example'],
)
def generateToken(**kwargs):
    auth_url = 'https://accounts.spotify.com/api/token'
    data = {
    'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    return requests.post(auth_url, data=data).json().get('access_token')

def viewData(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='extract_data')
    logging.info(data)

def extractData(**kwargs):
    ti = kwargs['ti']
    token = ti.xcom_pull(task_ids='generate_token')
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        'Authorization': 'Bearer {token}'.format(token=token)
    }
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000
    logging.info(f"time = {yesterday_unix_timestamp}")
    url = f"https://api.spotify.com/v1/me/player/recently-played?after={yesterday_unix_timestamp}"
    recently_played = requests.get(url=url, headers=headers).json()
    return recently_played

with dag:
    generate_token = PythonOperator(
        task_id='generate_token',
        python_callable=generateToken,
        provide_context=True,
    )
    extract_data = PythonOperator(
        task_id='extract_data',
        python_callable=extractData,
        provide_context=True,
    )

    view_data = PythonOperator(
        task_id='view_data',
        python_callable=viewData,
        provide_context=True,
    )

generate_token >> extract_data >> view_data
