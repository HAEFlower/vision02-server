import json
from openai import OpenAI

client = OpenAI()


def ask_chatgpt(ingredients: list, cooking_goal: str, cooking_method: str):
    messages = build_strict_prompt_messages(ingredients, cooking_goal, cooking_method, 4)

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
                                    "cookingTime": {
                                        "type": "string",
                                        "description": "레시피의 대략적인 요리 시간 (예: '15분')"
                                    },
                                },
                                "required": [
                                    "recipeTitle",
                                    "recipeDesc",
                                    "ingredientsUsed",
                                    "steps",
                                    "cookingTime"
                                ],
                            },
                        }
                    },
                    "required": ["recipes"],
                    "additionalProperties": False,
                },
            },
        },
        max_tokens=2048,
        temperature=0.4,
    )

    raw_json_str = response.choices[0].message.content
    parsed_json = json.loads(raw_json_str)
    return parsed_json


def build_strict_prompt_messages(
    ingredients: list,
    cooking_goal: str,
    cooking_method: str,
    max_recipes: int
):
    """
    ingredients: 예) ["계란", "우유", "생크림", "딸기"]
    cooking_goal: 예) "간식"
    cooking_method: 예) "디저트"
    max_recipes: 생성할 최대 레시피 수
    """

    prompt_messages = [
        {
            "role": "developer",
            "content": f"""
            You are a recipe generator.
            You will ONLY create recipes that match the provided cooking parameters:
            - Ingredients: {ingredients}
            - Cooking Goal: {cooking_goal}
            - Cooking Method: {cooking_method}

            Generate up to {max_recipes} valid JSON recipes.
            Each recipe must strictly use only the given ingredients, plus minimal common condiments (e.g., 소금, 설탕, 식용유 등).
            No additional or irrelevant ingredients beyond these are allowed.

            **REQUIREMENTS**:
            1) The output must be valid JSON and must include exactly up to {max_recipes} recipe objects, no extra text.
            2) Each recipe must follow the schema:
            - recipeTitle (string)
            - recipeDesc (string)
            - ingredientsUsed (array of strings)
            - steps (array of strings)
            - cookingTime (string, e.g., '15분')
            3) All ingredients or condiments that appear in steps MUST also appear in "ingredientsUsed".
            4) Conversely, any item in "ingredientsUsed" that is used in cooking should be mentioned in "steps".
            5) Each item in "ingredientsUsed" must include both the ingredient name and its amount (e.g., '우유 1컵').
            6) Number each step in "steps" (e.g., '1. 달걀을 깬다').
            7) The recipe content should be written in Korean.
            8) Do NOT output any text other than the JSON (no extra commentary or explanations).
            9) The recipes must be suitable for the given cooking goal and method. For example, if the method is 디저트, it should be a dessert recipe.
            10) Include the cookingTime field in each recipe to indicate approximate cooking duration.

            Remember: Do not include ingredients that are not listed in the user's input (beyond minor condiments), and do not produce irrelevant dishes.
            """
        },
        {
            "role": "user",
            "content": f"""
            Ingredients: {ingredients}
            Cooking Goal: {cooking_goal}
            Cooking Method: {cooking_method}

            JSON fields:
            - recipeTitle (string)
            - recipeDesc (string)
            - ingredientsUsed (array of strings)
            - steps (array of strings)
            - cookingTime (string, e.g., '15분')

            Please provide up to {max_recipes} recipe(s).
            Must be strictly limited to these ingredients (with minimal condiments).
            Output in Korean.
            No extra text besides the JSON.
            """
        }
    ]

    return prompt_messages




# 이미지 생성 보류
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

