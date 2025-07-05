import os
from openai import OpenAI

# Render 환경변수에서 API 키 읽기
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_ai_recommendation(query):
    try:
        prompt = f"""
당신은 건강 영양 전문가입니다.
'{query}'에 대해 아래 형식으로 설명해주세요:

1. 관련 건강 위험 요소 또는 결핍 설명

2. 추천 영양소 및 음식

3. 도움이 되는 생활 습관 및 주의 사항

4. 마무리 문장: 모든 정보는 참고용이며 전문가 상담이 필요합니다.

각 항목은 번호를 붙이고 보기 좋게 구성해주세요.
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 건강 영양 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ 오류가 발생했습니다: {e}"
