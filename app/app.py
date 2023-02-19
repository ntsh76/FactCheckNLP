from flask import Flask, render_template, request, flash, jsonify, redirect, url_for
from utils.scraper import get_source_text
from utils.model import model

app = Flask(__name__)
app.secret_key = "blah"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/fact-check", methods=["POST", "GET"])
def check():
    try:
        # Get user input
        claim = request.form["claim_input"]
        source = request.form["source_input"]
        # If user did not provide source, get one by searching Google
        if not source:
            source = get_source_text()
        # Update the result page with user claim
        flash(claim)

        # TODO Put machine learning model here
        result, confidence = model(claim, source)
        data = {"result": result, "confidence": confidence}

        return render_template("results.html", data=data)
    except Exception:
        return redirect(url_for("index"))


@app.route("/about")
def about():
    return render_template("about.html")
