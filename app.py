from flask import Flask, render_template, request
from utils.gpt import get_ai_recommendation
from dotenv import load_dotenv

# .env 환경변수 로드
load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    recommendation = ""
    if request.method == "POST":
        query = request.form.get("query")
        recommendation = get_ai_recommendation(query)
    return render_template("index.html", recommendation=recommendation)

@app.route("/about")
def about():
    return render_template("about.html")  # 경로 수정

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")  # 경로 수정

@app.route("/terms")
def terms():
    return render_template("terms.html")  # 경로 수정

