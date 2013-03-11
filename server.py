import sys
import os
import time
from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy


# Create our Flask app
#
app = Flask(__name__)
app.config.from_pyfile('config.py')


# Optionally, set up psycopg2 to be greenlet-friendly.
# (Note, it does not really monkey patch psycopg2 in
# the manner that gevent monkey patches socket.)
#
if "PSYCOGREEN" in os.environ:
    from psycogreen.gevent import patch_psycopg
    patch_psycopg()


# Set up our database using Flask-SQLAlchemy
#
db = SQLAlchemy(app)


class Todo(db.Model):
    """ Small example model just to show you that SQLAlchemy is
        doing everything it should be doing.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    done = db.Column(db.Boolean)
    priority = db.Column(db.Integer)

    def as_dict(self):
        """ Return an individual Todo as a dictionary.
        """
        return {
            'id': self.id,
            'title': self.title,
            'done': self.done,
            'priority': self.priority
        }

    @classmethod
    def jsonify_all(cls):
        """ Returns all Todo instances in a JSON
            Flask response.
        """
        return jsonify(todos=[todo.as_dict() for todo in cls.query.all()])


@app.route('/sleep/postgres/')
def sleep_postgres():
    """ This handler asks Postgres to sleep for 5s and will
        block for 5s unless psycopg2 is set up (above) to be
        gevent-friendly.
    """
    db.session.execute('SELECT pg_sleep(5)')
    return Todo.jsonify_all()


@app.route('/sleep/python/')
def sleep_python():
    """ This handler sleeps for 5s and will block for 5s unless
        gunicorn is using the gevent worker class.
    """
    time.sleep(5)
    return Todo.jsonify_all()


# Create the tables and populate it with some dummy data
#
def create_data():
    """ A helper function to create our tables and some Todo objects.
    """
    db.create_all()
    todos = []
    for i in range(50):
        todo = Todo(
            title="Slave for the man {0}".format(i),
            done=(i % 2 == 0),
            priority=(i % 5)
        )
        todos.append(todo)
    db.session.add_all(todos)
    db.session.commit()


if __name__ == '__main__':

    if '-c' in sys.argv:
        create_data()
    else:
        app.run()
