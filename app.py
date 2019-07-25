from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.j2")


@app.route("/<name>")
def hello(name):
    return f"Hello, {name}"
