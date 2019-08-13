from datetime import datetime
import json
from tornado_sqlalchemy import SessionMixin, as_future
from tornado.web import RequestHandler
from tornado.gen import coroutine
from todo.models import Profile, Task


class BaseView(RequestHandler, SessionMixin):
    """Base view for this application."""

    def prepare(self):
        self.form_data = {
            key: [val.decode('utf8') for val in val_list]
            for key, val_list in self.request.arguments.items()
        }

    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", "application/json; charset='utf-8'")

    def send_response(self, data, status=200):
        """Construct a send a JSON response with appropriate status code."""
        self.set_status(status)
        self.write(json.dumps(data))


class TaskListView(BaseView):
    """View for reading and adding new tasks."""
    SUPPORTED_METHODS = ("GET", "POST",)

    @coroutine
    def get(self, username):
        """Get all tasks for an existing user."""
        with self.make_session() as session:
            profile = yield as_future(session.query(Profile).filter(Profile.username == username).first)
            if profile:
                tasks = [task.to_dict() for task in profile.tasks]
                self.send_response({
                    "username": profile.username,
                    "tasks": tasks
                })

    @coroutine
    def post(self, username):
        """Create a new task."""
        with self.make_session() as session:
            profile = yield as_future(session.query(Profile).filter(Profile.username == username).first)
            if profile:
                due_date = self.form_data['due_date'][0]
                task = Task(
                    name=self.form_data['name'][0],
                    note=self.form_data['note'][0],
                    creation_date=datetime.now(),
                    due_date=datetime.strptime(due_date, "%d/%m/%Y %H:%M%S") if due_date else None,
                    completed=self.form_data['completed'][0],
                    profile_id=profile.id,
                    profile=profile,
                )
                session.add(task)
                self.send_response({"msg": "posted"}, status=201)


class InfoView(RequestHandler):
    """Only allow GET requests."""
    SUPPORTED_METHODS = ["GET"]

    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content_Type", "application/json; charset='utf-8'")

    def get(self):
        """List of routes for this API."""
        routes = {
            "info": "GET /api/v1",
            "register": "POST /api/v1/accounts",
            "single profile detail": "GET /api/v1/accounts/<username>",
            "edit profile": "PUT /api/v1/accounts/<username>",
            "delete profile": "DELETE /api/v1/accounts/<username>",
            "login": "POST /api/v1/accounts/login",
            "logout": "GET /api/v1/accounts/logout",
            "user's task": "GET /api/v1/accounts/<username>/tasks",
            "create task": "POST /api/v1/accounts/<username>/tasks",
            "task detail": "GET /api/v1/accounts/<username>/tasks/<id>",
            "task update": "PUT /api/v1/accounts/<username>/tasks/<id>",
            "delete task": "DELETE /api/v1/accounts/<username>/tasks/<id>",
        }
        self.write(json.dumps(routes))
