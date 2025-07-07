import os
from openai import OpenAI
from openai import OpenAIError

# Render 환경변수에서 API 키 읽기
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_ai_recommendation(query):
    try:
        prompt = f"""당신은 건강 영양 전문가입니다.

import os
from openai import OpenAI
from openai import OpenAIError

# Render 환경변수에서 API 키 읽기
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_ai_recommendation(query):
    try:
        prompt = f"""당신은 건강 영양 전문가입니다.

사용자가 입력한 '{query}'는 증상일 수도 있고, 영양소일 수도 있습니다. 
'{query}'가 증상일 경우 1번으로 작성하고 영양소일 경우 2번으로 작성해 주세요
ai로써 둘 중 하나로만 판단하여 친절하고 자연스럽게 설명해 주세요. 
아래 항목에 해당하는 내용을 모두 포함하되, 
제목 없이 ✅ 표시만 붙이고 각 항목 사이에는 한 줄 공백을 넣어 출력하세요. 
제목, 분기 안내문 따옴표 등을 출력하지 마세요
중복 출력은 하지 말고, 반드시 1번과 2번 둘 중 하나로만 작성해 주세요.
-출력시 가장 위에 '{query}'가 증상일 경우,  '{query}'가 영양소일 경우 이 글들은 절대 출력하지 않습니다.

-1번  '{query}'가 증상일 경우:
✅ 요약 설명과 원인

✅ 필요한 영양소

✅ 도움이 되는 음식

✅ 도움이 되는 생활 습관

✅  모든 정보는 참고용이며, '{query}'에 대한 증상이 지속되면 전문가 상담이 필요합니다.

-2번 '{query}'가 영양소일 경우:
✅ 주요 특징과 우리 몸에 주는 도움

✅ 부족 시 증상

✅ 많이 들어 있는 음식

✅ 효과적인 섭취 방법

✅ 모든 정보는 참고용이며, '{query}'이 부족하다고 느껴지면 전문가 상담이 필요합니다.

※ 첫 문장은 들여쓰기 없이 출력하고, 각 줄 맨 앞에는 ✅ 만 붙이세요. 제목은 작성하지 마세요.


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




