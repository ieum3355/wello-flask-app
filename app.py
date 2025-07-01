from dotenv import load_dotenv
import os
from flask import Flask, render_template, request
from utils.gpt import get_ai_recommendation

# .env 환경변수 로드
load_dotenv()

app = Flask(__name__)

# 홈 페이지
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        query = request.form["query"].strip()
        if query:
            result = get_ai_recommendation(query)
    return render_template("index.html", result=result)

# 결과 페이지 (선택 사항)
@app.route("/result/<keyword>")
def result(keyword):
    return render_template("result.html", title=keyword, description=f"{keyword}에 대한 설명입니다.")

# 개인정보 처리방침
@app.route("/privacy")
def privacy():
    return render_template("legal/privacy.html")

# 이용약관
@app.route("/terms")
def terms():
    return render_template("legal/terms.html")

# 소개 페이지
@app.route("/about")
def about():
    return render_template("legal/about.html")

# ⚠️ 아래 부분은 배포 환경에선 제거합니다.
# if __name__ == "__main__":
#     app.run(debug=True)
