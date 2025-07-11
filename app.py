from flask import Flask, render_template, request, send_from_directory
from dotenv import load_dotenv
from utils.gpt import get_ai_recommendation

load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    recommendation = ""
    if request.method == "POST":
        query = request.form.get("query", "")
        recommendation = get_ai_recommendation(query)
    return render_template("index.html", recommendation=recommendation)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/ads.txt")
def ads():
    return send_from_directory("static", "ads.txt")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/robots.txt")
def robots():
    return send_from_directory("static", "robots.txt")

@app.route("/blog")
def blog():
    posts = [
        {"title": "탈모에 좋은 음식 5가지", "slug": "hair-loss-foods"},
        {"title": "스트레스 완화에 효과적인 영양소", "slug": "stress-nutrients"},
        {"title": "면역력 강화 식품 리스트", "slug": "immune-foods"},
        {"title": "피로 회복에 좋은 음식", "slug": "fatigue-foods"},
        {"title": "집중력 향상에 도움 되는 영양소", "slug": "focus-nutrients"},
        {"title": "피부 건강에 좋은 영양소", "slug": "skin-health-nutrients"},
        {"title": "다이어트에 효과적인 음식", "slug": "diet-foods"},
        {"title": "수면의 질을 높이는 음식", "slug": "sleep-foods"},
        {"title": "장 건강에 좋은 식품", "slug": "gut-health-foods"},
        {"title": "감기 예방을 위한 영양소", "slug": "cold-prevention"}
    ]
    return render_template("blog.html", posts=posts)

@app.route("/blog/<slug>")
def blog_post(slug):
    return render_template(f"posts/{slug}.html")

@app.after_request
def disable_caching(response):
    response.headers["Cache-Control"] = "no-store"
    return response

if __name__ == "__main__":
    app.run(debug=True)
