import os
from openai import OpenAI
from openai import OpenAIError

# Render 환경변수에서 API 키 읽기
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_ai_recommendation(query):
    try:
        prompt = f"""
당신은 건강 영양 전문가입니다.

'{query}'는 증상일 수도 있고 영양소일 수도 있습니다. 사용자가 입력한 '{query}'가 어떤 항목인지 파악한 후 다음 형식 중 하나에 따라 자연스럽고 친절하게 작성해 주세요.

✅ {query}에 대한 요약 설명과 원인을 알려주세요

✅ 필요한 영양소를 알려주세요

✅ 도움이 되는 음식을 알려주세요

✅ 완화에 도움이 되는 생활 습관을 알려주세요

✅ 모든 정보는 참고용이며, '{query}' 증상이 심각하거나 지속될 경우 전문가 상담이 필요합니다.



✅ {query}의 주요 특징 및 우리 몸에 어떤 도움을 주는지 알려주세요

✅ 부족할 경우 나타나는 증상을 알려주세요

✅ 많이 들어 있는 음식들을 알려주세요

✅ 효과적으로 얻기 위한 생활 습관을 알려주세요

✅ 모든 정보는 참고용이며, '{query}' 부족이 심각하다 생각될 경우 전문가 상담이 필요합니다.

※ 각 항목 앞에 "✅" 표시만 붙이고, 제목이나 설명 없이 자연스럽게 문장을 작성해 주세요.
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

