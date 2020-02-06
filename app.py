import logging

from flask import Flask
from lagom import Container, bind_to_container, Singleton

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = Flask(__name__)


# This is our database
class Database:
    def __init__(self, dsn):
        self.dsn = dsn

    def save(self, stuff):
        log.info(f"I would have saved: '{stuff}' to '{self.dsn}'")


# Define the configuration for our database
container = Container()
container[Database] = Singleton(lambda: Database("connection details"))


# Define the routes the app handles
@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/save_it/<string:thing_to_save>", methods=['GET', 'POST'])
@bind_to_container(container)
def save_to_db(thing_to_save, db: Database):
    db.save(thing_to_save)
    return 'saved'


# Run the app
if __name__ == '__main__':
    app.run()
