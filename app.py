# app.py

from flask import Flask, render_template, request
from dotenv import load_dotenv
from utils.gpt import get_ai_recommendation
import os

# .env 파일 로드
load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        query = request.form["query"].strip()
        if query:
            result = get_ai_recommendation(query)
    return render_template("index.html", result=result)

@app.route("/result/<keyword>")
def result(keyword):
    return render_template("result.html", title=keyword, description=f"{keyword}에 대한 설명입니다.")

@app.route("/privacy")
def privacy():
    return render_template("legal/privacy.html")

@app.route("/terms")
def terms():
    return render_template("legal/terms.html")

@app.route("/about")
def about():
    return render_template("legal/about.html")
