import os
from openai import OpenAI
from openai import OpenAIError

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_ai_recommendation(query):
    try:
        # 1단계: 쿼리 유형 판단 (증상인지 영양소인지)
        classification_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "당신은 건강 관련 단어를 분석하는 전문가입니다."},
                {"role": "user", "content": f"'{query}'는 건강 관련 단어입니다. 이것이 '증상'인지 '영양소'인지 딱 한 단어로만 답해주세요."}
            ],
            functions=[
                {
                    "name": "classify_query",
                    "description": "입력된 단어가 증상인지 영양소인지 판단",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "type": {
                                "type": "string",
                                "enum": ["증상", "영양소"],
                                "description": "입력된 단어의 분류 결과"
                            }
                        },
                        "required": ["type"]
                    }
                }
            ],
            function_call={"name": "classify_query"},
            temperature=0
        )

        query_type = classification_response.choices[0].message.function_call.arguments
        query_type = eval(query_type)['type']

        # 2단계: 해당 타입에 따라 상세 설명 생성
        if query_type == "증상":
            prompt = f"""
당신은 건강 영양 전문가입니다.

'{query}'는 증상입니다. 아래 항목을 ✅로 시작하며, 항목마다 줄 간격을 넣어 자연스럽게 설명해 주세요. 제목 없이 ✅만 붙이세요.

✅ 요약 설명과 원인

✅ 필요한 영양소

✅ 도움이 되는 음식

✅ 도움이 되는 생활 습관

✅ 모든 정보는 참고용이며, '{query}'에 대한 증상이 지속되면 전문가 상담이 필요합니다.
"""
        else:  # 영양소일 경우
            prompt = f"""
당신은 건강 영양 전문가입니다.

'{query}'는 영양소입니다. 아래 항목을 ✅로 시작하며, 항목마다 줄 간격을 넣어 자연스럽게 설명해 주세요. 제목 없이 ✅만 붙이세요.

✅ 주요 특징과 우리 몸에 주는 도움

✅ 부족 시 증상

✅ 많이 들어 있는 음식

✅ 효과적인 섭취 방법

✅ 모든 정보는 참고용이며, '{query}'이(가) 부족하다고 느껴지면 전문가 상담이 필요합니다.

* 마지막 주의 문구는 한 줄만 작성하고, 추가적인 경고나 설명은 하지마세요.

* 첫 문장을 들여쓰기 없이 출력해주세요.
"""

        detail_response = client.chat.completions.create(
           model="gpt-4o",
           messages=[
                {"role": "system", "content": "당신은 건강 영양 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        return detail_response.choices[0].message.content.strip()

    except OpenAIError as e:
        return f"⚠️ 오류 발생: {str(e)}"



