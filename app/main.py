from flask import Flask, jsonify

from db import get_session

app = Flask(__name__)
session = get_session()


def _chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


@app.route("/")
def index():
    return "<h1>Welcome...to MismatchBot</h1>"


@app.route("/records/", methods=["GET"])
def records():
    from models import Character, Record, Stage
    from use_cases.frame_conversion import frames_to_time_string

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
    return jsonify(list(chunked_data))
