import flask
app = flask.Flask(__name__)


@app.route("/")
def index():
    return "Welcome to SPM Team 4's Page "