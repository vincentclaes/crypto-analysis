"""WSGI entrypoint for gunicorn et al."""

from app import app
from gevent.wsgi import WSGIServer
http_server = WSGIServer(('', 80), app)
http_server.serve_forever()