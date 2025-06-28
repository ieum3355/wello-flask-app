from flask import Flask, render_template, request

app = Flask(__name__)

# 증상 → 추천 영양소
symptom_to_nutrient = {
    "눈 피로": ["비타민 A", "오메가3"],
    "탈모": ["비오틴", "아연", "비타민 D"],
    "피로감": ["비타민 B12", "철분", "마그네슘"],
    "면역력 저하": ["비타민 C", "아연"]
}

# 영양소 → 연관 증상
nutrient_to_symptom = {
    "오메가3": ["눈 피로", "심혈관 건강", "뇌 기능 저하"],
    "비오틴": ["탈모", "손톱 갈라짐", "피부 트러블"],
    "아연": ["면역력 저하", "탈모"],
    "비타민 C": ["감기 잦음", "피부 재생력 저하"]
}

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        query = request.form["query"].strip()
        if query in symptom_to_nutrient:
            result = f"💊 '{query}' 증상에 추천되는 영양소: " + ", ".join(symptom_to_nutrient[query])
        elif query in nutrient_to_symptom:
            result = f"🩺 '{query}'는 다음 증상에 도움이 됩니다: " + ", ".join(nutrient_to_symptom[query])
        else:
            result = "❌ 해당 항목에 대한 정보를 찾을 수 없습니다."
    return render_template("index.html", result=result)
