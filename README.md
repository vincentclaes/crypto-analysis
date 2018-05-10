sudo fuser -k 80/tcp
sudo fuser -k 5004/tcp

sudo nohup python app_wsgi.py 
sudo nohup python endpoints_wsgi.py 

