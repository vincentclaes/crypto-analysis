"""WSGI entrypoint for gunicorn et al."""

from app import app
from gevent.wsgi import WSGIServer
http_server = WSGIServer(('', 8080), app)
http_server.serve_forever()