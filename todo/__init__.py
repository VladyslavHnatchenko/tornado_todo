from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
from todo.views import InfoView

import os
from tornado_sqlalchemy import make_session_factory


define('port', default=8888, help="port to listen on")
factory = make_session_factory(os.environ.get("DATABASE_URL", ""))


def main():
    """Construct and serve the tornado application."""
    app = Application([
        ("/", InfoView)
    ],
        sesion_factory=factory
    )
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    print("Listening on http://localhost:%i" % options.port)
    IOLoop.current().start()
