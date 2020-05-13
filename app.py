import logging

from flask import Flask
from lagom import Singleton
from lagom.integrations.flask import FlaskContainer

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = Flask(__name__)


# This is the code for our DB - in a real example this would likely be from a DB library.
class Database:
    def __init__(self, dsn):
        self.dsn = dsn

    def save(self, stuff):
        log.info(f"I would have saved: '{stuff}' to '{self.dsn}'")


# Define the configuration for our app. Setting how our database is loaded.
# In this case we're explicit about it being a singleton.
container = FlaskContainer(app)
container[Database] = Singleton(lambda: Database("connection details"))


# Define the routes the app handles
@container.route('/')
def hello_world():
    return 'Hello World!'


@container.route("/save_it/<string:thing_to_save>", methods=['GET', 'POST'])
def save_to_db(thing_to_save, db: Database):
    # Note: the signature above tells us everything the function needs. There's no global dependeance. 
    # without looking in the body of the method we can tell what the function will interact with.
    db.save(thing_to_save)
    return 'saved'


# Run the app
if __name__ == '__main__':
    app.run()
