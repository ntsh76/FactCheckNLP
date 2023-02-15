from flask import Flask, render_template, request, flash, jsonify, redirect, url_for
from utils.scrape import get_source_text
from utils.model import model

app = Flask(__name__)
app.secret_key = "blah"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/fact-check", methods=["POST", "GET"])
def check():
    try:
        claim = request.form["claim_input"]
        flash(claim)
        source = request.form["source_input"]
        if not source:
            source = get_source_text()

        # TODO Put machine learning model here
        result, confidence = model(claim, source)
        data = {"result": result, "confidence": confidence}

        return render_template("results.html", data=data)
    except Exception:
        return redirect(url_for("index"))


@app.route("/about")
def about():
    return render_template("about.html")
