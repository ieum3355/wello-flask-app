import os
from openai import OpenAI
from openai import OpenAIError
import time

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    timeout=30.0  # 30 second timeout to prevent hanging
)

def get_ai_recommendation(query):
    """
    Optimized single-call approach that determines query type and generates response in one API call
    """
    start_time = time.time()
    
    try:
        # Single optimized prompt that handles both classification and response generation
        optimized_prompt = f"""
당신은 건강 영양 전문가입니다.

'{query}'에 대해 분석해주세요. 이것이 건강 증상인지 영양소인지 자동으로 판단하고, 해당하는 형식으로 답변해주세요.

**증상인 경우 형식:**
✅ 요약 설명과 원인

✅ 필요한 영양소

✅ 도움이 되는 음식

✅ 도움이 되는 생활 습관

✅ 모든 정보는 참고용이며, '{query}'에 대한 증상이 지속되면 전문가 상담이 필요합니다.

**영양소인 경우 형식:**
✅ 주요 특징과 우리 몸에 주는 도움

✅ 부족 시 증상

✅ 많이 들어 있는 음식

✅ 효과적인 섭취 방법

✅ 모든 정보는 참고용이며, '{query}'이(가) 부족하다고 느껴지면 전문가 상담이 필요합니다.

각 항목마다 줄 간격을 넣어 자연스럽게 설명해 주세요. 제목 없이 ✅만 붙이고, 들여쓰기 없이 출력해주세요.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use faster, cheaper model for better performance
            messages=[
                {
                    "role": "system", 
                    "content": "당신은 건강 영양 전문가입니다. 간결하고 정확한 정보를 제공하며, 입력된 단어가 증상인지 영양소인지 자동으로 판단하여 적절한 형식으로 답변합니다."
                },
                {"role": "user", "content": optimized_prompt}
            ],
            temperature=0.3,  # Lower temperature for more consistent responses
            max_tokens=1500,  # Limit response length for faster processing
            presence_penalty=0.1  # Encourage concise responses
        )

        result = response.choices[0].message.content.strip()
        
        # Log performance metrics (can be removed in production)
        elapsed_time = time.time() - start_time
        print(f"AI response generated in {elapsed_time:.2f} seconds")
        
        return result

    except OpenAIError as e:
        error_msg = f"⚠️ AI 서비스 오류: 잠시 후 다시 시도해주세요."
        print(f"OpenAI API Error: {str(e)}")
        return error_msg
    
    except Exception as e:
        error_msg = f"⚠️ 서비스 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
        print(f"Unexpected error: {str(e)}")
        return error_msg

# Additional helper function for future async optimization
def get_ai_recommendation_with_fallback(query, max_retries=2):
    """
    Enhanced version with retry logic for production use
    """
    for attempt in range(max_retries):
        try:
            result = get_ai_recommendation(query)
            if not result.startswith("⚠️"):
                return result
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(1)  # Brief delay before retry
    
    return "⚠️ 서비스가 일시적으로 불안정합니다. 잠시 후 다시 시도해주세요."



