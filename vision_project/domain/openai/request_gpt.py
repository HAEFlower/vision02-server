import json
from openai import OpenAI

client = OpenAI()


def ask_chatgpt(ingredients: list, cooking_goal: str, cooking_method: str):
    messages = [
        {
            "role": "developer",
            "content": (
                "You will be given cooking parameters.\n"
                "Reply with exactly 4 recipes in valid JSON, following the schema below.\n"
                "For korean\n"
                "IMPORTANT:\n"
                "1) All ingredients (including condiments, sauces, spices, etc.) in steps MUST also appear in 'ingredientsUsed'.\n"
                "2) Conversely, any item in 'ingredientsUsed' that is used in cooking should be mentioned in steps.\n"
                "3) Do NOT output any additional text other than JSON.\n"
            ),
        },
        {
            "role": "user",
            "content": (
                f"Ingredients: {ingredients}\n"
                f"Cooking Goal: {cooking_goal}\n"
                f"Cooking Method: {cooking_method}\n\n"
                "JSON fields:\n"
                "- recipeTitle (string)\n"
                "- recipeDesc (string)\n"
                "- ingredientsUsed (array of strings)\n"
                "- steps (array of strings)\n"
                "Please provide exactly 4 recipes.\n"
                "Again, if any item (like butter) is used in steps, it must be in ingredientsUsed."
            ),
        },
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # 실제 사용 가능 모델명으로 교체
        messages=messages,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "recipes_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "recipes": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "recipeTitle": {
                                        "type": "string",
                                        "description": "요리 이름",
                                    },
                                    "recipeDesc": {
                                        "type": "string",
                                        "description": "간단 설명",
                                    },
                                    "ingredientsUsed": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "모든 식재료 + 조미료. steps에 언급된 것은 반드시 포함",
                                    },
                                    "steps": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "조리 순서. ingredientsUsed에 기재된 항목은 여기에도 최소 한 번 등장",
                                    },
                                },
                                "required": [
                                    "recipeTitle",
                                    "recipeDesc",
                                    "ingredientsUsed",
                                    "steps",
                                ],
                            },
                        }
                    },
                    "required": ["recipes"],
                    "additionalProperties": False,
                },
            },
        },
        max_tokens=1024,
        temperature=0.4,
    )

    raw_json_str = response.choices[0].message.content
    parsed_json = json.loads(raw_json_str)
    return parsed_json

def generate_image_prompt(food_name: str) -> str:
    prompt = f"Generate a detailed artistic description to create an image of a delicious {food_name}."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    return response.choices[0].message.content

def get_image(dish_name: str):
    """
    dish_name: 요리 이름, 예) "김치볶음밥", "에그베네딕트" 등
    """

    prompt_text = generate_image_prompt(dish_name)

    response = client.images.generate(
        model="dall-e-2",
        prompt=prompt_text,
        size="256x256",
        quality="standard",
        n=1
    )

    return response.data[0].url

