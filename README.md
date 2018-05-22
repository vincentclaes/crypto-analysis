# COMMANDS

## init

add to .bashrc

`export LC_ALL=C`

install pipenv

`pip install pipenv`

airflow

`mkdir airflow`
`cd airflow`
`pipenv --two`
`pipenv shell`
`pipenv install airflow`
`airflow webserver -p 8080`
`airflow scheduler`

## start
`sudo nohup python app_wsgi.py`

`sudo nohup python endpoints_wsgi.py`

## stop
`sudo fuser -k 80/tcp`

`sudo fuser -k 5004/tcp`




