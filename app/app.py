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
            try:
                source = get_source_text(claim)
            except Exception as e:
                source = ""
        # Update the result page with user claim
        flash("Claim: " + claim)

        result, confidence, explanation = model(claim, source)
        if not source:
            confidence = 0
            explanation = "No source provided or source lookup failed"
        data = {"result": result, "confidence": confidence, "explanation": explanation}

        return render_template("results.html", data=data)
    except Exception as e:
        return redirect(url_for("index"))


@app.route("/about")
def about():
    return render_template("about.html")
