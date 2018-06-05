"""
WSGI entrypoint for gunicorn et al.

before we used:

from gevent.wsgi import WSGIServer
http_server = WSGIServer(('', 5004), app)
http_server.serve_forever()

but this couldn't handle concurrent requests.
now we start the app with

gunicorn endpoints_wsgi:app -k gevent -w 2 -b 0.0.0.0:5004

"""

from endpoints import app

app
