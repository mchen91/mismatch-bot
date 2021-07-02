from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS, cross_origin

from db import get_session

app = Flask(__name__, static_folder="../frontend/build", static_url_path="")
cors = CORS(app)
session = get_session()


def _chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/records/", methods=["GET"])
def records():
    from models import Character, Record, Stage

    all_records = (
        session.query(Record)
        .join(Character)
        .join(Stage)
        .filter(Character.position < 25, Stage.position < 25)
        .order_by(Character.position, Stage.position)
        .all()
    )
    data = [
        {
            "value": record.partial_targets if record.time is None else record.time,
            "is_partial": record.time is None,
        }
        for record in all_records
    ]
    chunked_data = _chunks(data, 25)
    response = jsonify(list(chunked_data))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0")
