"""
WSGI entrypoint for gunicorn et al.

before we used:

from gevent.wsgi import WSGIServer
http_server = WSGIServer(('', 80), app)
http_server.serve_forever()

but this couldn't handle concurrent requests.
now we start the app with

gunicorn app_wsgi:app -k gevent -w 2 -b 0.0.0.0:80

"""

from app import app
app
