import os
from openai import OpenAI
from openai import OpenAIError

# Render 환경변수에서 API 키 읽기
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_ai_recommendation(query):
    try:
        prompt = f"""
당신은 건강 영양 전문가입니다.
'{query}'에 대해 아래 형식으로 설명해주세요:

1. 관련 건강 위험 요소 또는 결핍 내용을 간단하고 명확하게 작성해주세요 (제목 없이 설명만 출력).

2. 추천 영양소와 관련 음식 정보를 다음 형식으로 작성해주세요 (제목 없이 출력):
- 추천 영양소: 예) 비타민D, 오메가3 등
- 관련 음식: 예) 고등어, 브로콜리 등

3. 생활 습관이나 주의사항을 자연스럽게 작성하되 제목 없이 번호만 붙여 출력해주세요.

4. 아래 문장을 그대로 출력해주세요:
모든 정보는 참고용이며, '{query}' 증상이 심각하거나 지속적일 경우 전문가 상담이 필요합니다.

※ 모든 항목에는 제목이나 굵은 글씨 없이 숫자 뒤에 바로 내용을 자연스럽게 출력해주세요.
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

    except OpenAIError as e:
        return f"⚠️ 오류 발생: {str(e)}"


