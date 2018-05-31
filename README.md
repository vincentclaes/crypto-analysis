# COMMANDS

## init

add to .bashrc

`export LC_ALL=C`

install pipenv

`pip install pipenv`

### airflow

#### start
`mkdir airflow`
`cd airflow`
`pipenv --two`
`pipenv shell`
`sudo yum install gcc-c++ python-devel python-setuptools`
`pipenv install airflow`
`airflow initdb`
`nohup airflow webserver -p 8080 >& /dev/null < /dev/null &`
`nohup airflow scheduler >& /dev/null < /dev/null &`

#### stop

`kill $(ps -ef | grep "airflow scheduler" | awk '{print $2}')`
`sudo fuser -k 8080/tcp`


### mongo


follow steps here https://docs.mongodb.com/manual/tutorial/install-mongodb-on-amazon/


`sudo mkdir /data/db`
`sudo mongod`

### sqlite

`mkdir ~/projects/data`
`scp -i ~/.ssh/crypto-delta.pem coinmarketcap_data.db ec2-user@18.196.37.245:~/projects/data/coinmarketcap_data.db`

### front end + back end

#### start
`sudo nohup python app_wsgi.py >& /dev/null < /dev/null &`

`sudo nohup python endpoints_wsgi.py  >& /dev/null < /dev/null &`

#### stop
`sudo fuser -k 80/tcp`

`sudo fuser -k 5004/tcp`




