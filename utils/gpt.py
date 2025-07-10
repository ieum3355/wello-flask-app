import os
import time
from openai import OpenAI
from openai import OpenAIError

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_ai_recommendation(query):
    try:
        # Combined prompt that handles both classification and generation in one API call
        combined_prompt = f"""
당신은 건강 영양 전문가입니다. '{query}'에 대한 건강 정보를 제공해주세요.

먼저 '{query}'가 증상인지 영양소인지 판단한 후, 해당하는 형식으로 답변해주세요.

**증상인 경우:**
✅ 요약 설명과 원인
✅ 필요한 영양소
✅ 도움이 되는 음식
✅ 도움이 되는 생활 습관
✅ 모든 정보는 참고용이며, '{query}'에 대한 증상이 지속되면 전문가 상담이 필요합니다.

**영양소인 경우:**
✅ 주요 특징과 우리 몸에 주는 도움
✅ 부족 시 증상
✅ 많이 들어 있는 음식
✅ 효과적인 섭취 방법
✅ 모든 정보는 참고용이며, '{query}'이(가) 부족하다고 느껴지면 전문가 상담이 필요합니다.

답변은 ✅로 시작하며, 항목마다 줄 간격을 넣어 자연스럽게 설명해 주세요. 제목 없이 ✅만 붙이세요.
"""

        # Single API call with optimized parameters
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "당신은 건강 영양 전문가입니다. 정확하고 유용한 정보를 제공하세요."},
                {"role": "user", "content": combined_prompt}
            ],
            temperature=0.3,  # Lower temperature for more consistent output
            max_tokens=1000,  # Limit response length for faster processing
            timeout=30  # 30 second timeout
        )

        return response.choices[0].message.content.strip()

    except OpenAIError as e:
        return f"⚠️ AI 서비스 오류: {str(e)}"
    except Exception as e:
        return f"⚠️ 시스템 오류가 발생했습니다. 잠시 후 다시 시도해주세요."



