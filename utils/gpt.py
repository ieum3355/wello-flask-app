# utils/gpt.py

from openai import OpenAI
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 클라이언트 생성 (최신 방식)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_recommendation(query):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 건강 영양 전문가입니다."},
                {"role": "user", "content": f"{query}에 도움이 되는 영양소를 추천해줘."}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ 오류가 발생했습니다: {e}"
