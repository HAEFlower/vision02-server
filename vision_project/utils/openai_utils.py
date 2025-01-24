import os
import openai

# 환경 변수 설정 예시 (export OPENAI_API_KEY="sk-xxxx")
openai.api_key = os.environ.get("OPENAI_API_KEY", None)

def ask_chatgpt(prompt: str, max_tokens=50):
    """
    ChatGPT API를 호출해 답변을 반환합니다.
    gpt-3.5-turbo 엔진을 예시로 사용.
    """
    if openai.api_key is None:
        raise ValueError("OpenAI API 키가 설정되지 않았습니다.")
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.7
    )
    answer = response["choices"][0]["message"]["content"]
    return answer