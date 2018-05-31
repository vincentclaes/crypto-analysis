"""WSGI entrypoint for gunicorn et al."""

from endpoints import app
from gevent.wsgi import WSGIServer
http_server = WSGIServer(('', 5004), app, spawn=4)
http_server.serve_forever()