from openai import OpenAI

client = OpenAI()

def extract_product_names(receipt_text: str):
    """
    receipt_text: 영수증의 전체 텍스트
    """
    prompt = (
        "Extract product names from the given receipt text. "
        "Only return the product names as a list. "
        "Exclude company names. "
        "For Korean product names, infer and extract only the core ingredient names. "
        "For example, if the product name is '아삭콩나물', extract '콩나물'."
    )
    
    messages = [
        {"role": "user", "content": f"Receipt Text: {receipt_text}\n{prompt}"}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=200
    )

    product_names = response.choices[0].message.content.strip().split("\n")
    return product_names