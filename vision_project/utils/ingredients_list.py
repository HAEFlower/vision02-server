INGREDIENTS = [
    "onion",  # 0
    "carrot",  # 1
    "radish",  # 2
    "spinach",  # 3
    "green onion",  # 4
    "garlic",  # 5
    "potato",  # 6
    "sweet potato",  # 7
    "bell pepper",  # 8
    "paprika",  # 9
    "cabbage",  # 10
    "lettuce",  # 11
    "cucumber",  # 12
    "eggplant",  # 13
    "zucchini",  # 14
    "chili",  # 15
    "bean sprouts",  # 16
    "mushroom",  # 17
    "sesame leaf",  # 18
    "napa cabbage",  # 19
    "seaweed",  # 20
    "apple",  # 21
    "banana",  # 22
    "lemon",  # 23
    "chicken breast",  # 24
    "pork",  # 25
    "beef",  # 26
    "salmon",  # 27
    "shrimp",  # 28
    "tuna",  # 29
    "mackerel",  # 30
    "bacon",  # 31
    "sausage",  # 32
    "ham",  # 33
    "milk",  # 34
    "yogurt",  # 35
    "cheese",  # 36
    "cream cheese",  # 37
    "butter",  # 38
    "egg",  # 39
    "rice",  # 40
    "brownrice",  # 41
    "tofu",  # 42
    "soybean",  # 43
    "blackbean",  # 44
    "ramyeon",  # 45
    "kimchi",  # 46
    "bread",  # 47
    "dumpling",  # 48
    "clam",  # 49
]


def get_ingredient_by_id(ingredient_id: int) -> str:
    return INGREDIENTS[ingredient_id]


def get_ingreidients_list_by_ids(ids: list) -> list:
    return [get_ingredient_by_id(ingredient_id) for ingredient_id in ids]
