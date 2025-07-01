import openai
import os
from dotenv import load_dotenv

# 로컬 개발 환경에서만 사용되는 .env 파일 로딩
load_dotenv()

# 환경 변수에서 OpenAI API 키 가져오기
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_ai_recommendation(query):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 건강 영양 전문가입니다."},
                {"role": "user", "content": f"{query}에 도움이 되는 영양소를 추천해줘."}
            ],
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"⚠️ 오류가 발생했습니다: {e}"
