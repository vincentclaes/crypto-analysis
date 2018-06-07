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

move to ec2

`mkdir ~/projects/data`
`scp -i ~/.ssh/crypto-delta.pem coinmarketcap_data.db ec2-user@18.196.37.245:~/projects/data/coinmarketcap_data.db`

manually move it locally 

scp -i ~/.ssh/crypto-delta.pem ec2-user@18.196.37.245:~/projects/data/coinmarketcap_data.db coinmarketcap_data.db

### nginx

documentation: https://medium.com/ymedialabs-innovation/deploy-flask-app-with-nginx-using-gunicorn-and-supervisor-d7a93aa07c18

`sudo yum install nginx -y`

add following config to file

`sudo vim /etc/nginx/conf.d/virtual.conf`

```
server {
    listen       80;
    server_name  deltacryptoclub.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

`sudo service nginx restart`
`sudo service nginx start`
`sudo service nginx stop`

### front end + back end

#### start

we use gunicorn together with nginx to run the front end.
for the back end we use the regular command with gevent and wsgi server.

gevent + wsgi server
`sudo nohup python app_wsgi.py >& /dev/null < /dev/null &`
`sudo nohup python endpoints_wsgi.py  >& /dev/null < /dev/null &`

gunicorn and nginx
`nohup gunicorn app_wsgi:app -k gevent -w 2 -b 0.0.0.0:8000  >& /dev/null < /dev/null &`
`nohup gunicorn endpoints_wsgi:app -k gevent -w 2 -b 0.0.0.0:5004 >& /dev/null < /dev/null &`

#### stop
`sudo fuser -k 80/tcp`

`sudo fuser -k 5004/tcp`




