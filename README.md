# Airflow demo

For the purposes of this demo I will be using Ubuntu 20.20 and Python 3.8.8. 
Airflow does not work on Windows currently. 

## 0. Setup and enter a virtual environment  
execute in shell 1 and 2
```shells
python -m venv venv
source venv/bin/activate
```

## 1. Set `AIRFLOW_HOME`
execute in shell 1 and 2
```shell
export AIRFLOW_HOME=`pwd`/airflow
```

### 1.1 (Optional) Set `AIRFLOW__CORE__LOAD_EXAMPLES` to false 

```shell
export AIRFLOW__CORE__LOAD_EXAMPLES=false
```

## 2. Install Airflow

```shell
pip install apache-airflow
```

## 3. Initialise database with an user

```shell
airflow db init

airflow users create \
    --username Airflow \
    --firstname Airflow \
    --lastname Airflow \
    --role Admin \
    --password airflow \
    --email airflow@gmail.com
```

## 4. Start the services 

Use two different terminals, remember to activate your Python environment and set the environment variables!

### 4.1 Start the web server

```shell
airflow webserver --port 8080
```

### 4.2 Start the web server

```shell
airflow scheduler
```

## 5. Add a dags folder   

Inside the `$AIRFLOW_HOME` folder  

```shell
mkdir $AIRFLOW_HOME/dags
```

## 6. Add your first DAG

Create a file `first.py` in the newly created folder

### 6.1 Add imports

```python
from datetime import timedelta

from airflow import DAG

from airflow.operators.python import PythonOperator
```


