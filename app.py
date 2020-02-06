import logging
from flask import Flask

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = Flask(__name__)


class DatabaseOrWhatever:
    def save(self, stuff):
        log.info(f"I would have saved: {stuff}")


global_db = DatabaseOrWhatever()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/save_it/<string:thing_to_save>", methods=['GET', 'POST'])
def save_to_db(thing_to_save):
    global_db.save(thing_to_save)
    return 'saved'


if __name__ == '__main__':
    app.run()
