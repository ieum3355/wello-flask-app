# utils/gpt.py
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_ai_recommendation(query):
    try:
        prompt = f"""
당신은 건강 영양 전문가입니다.
사용자가 '{query}'라는 증상이나 건강 목표를 입력하면 다음 형식에 따라 답변하세요:

1. {query}와 관련된 건강 위험 요소 또는 영양 결핍 설명

2. 도움이 되는 음식 목록

3. 도움이 되는 생활 습관 및 주의 사항

4. 마무리 문장: 모든 추천 정보는 참고용으로 제공되며, 건강 문제는 반드시 전문가의 상담을 받으시기 바랍니다.

각 항목은 번호를 붙이고 항목 사이에 한 줄씩 띄워서 가독성 좋게 작성하세요.
"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 건강 영양 전문가입니다."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        return f"⚠️ 오류가 발생했습니다: {e}"

