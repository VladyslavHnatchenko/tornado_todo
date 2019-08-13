from datetime import datetime

from sqlalchemy.testing import db
from tornado_sqlalchemy import declarative_base
# from .app import db


Base = declarative_base


class Task(Base):
    """Task for the to-Do List."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False)
    note = db.Column(db.Unicode)
    creation_date = db.Column(db.DateTime, nullable=False)
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, *args, **kwargs):
        """On constructionn, set date of creation."""
        super().__init__(*args, **kwargs)
        self.creation_date = datetime.now()
