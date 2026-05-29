import json

def add_length_types():
    with open("prompts.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    for d in data["prompts"]:
        length = d["length"]
        length_type = ""

        if length <= 249:
            length_type = "shortest"
        elif length <= 349:
            length_type = "short"
        elif length <= 999:
            length_type = "average"
        elif length <= 1999:
            length_type = "long"
        elif length <= 2999:
            length_type = "longest"

        if "length type" not in d:
            d["length type"] = length_type
        else:
            d["length type"] = length_type

    with open("prompts.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)

def add_prompt_names():
    with open("prompts.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    for d in data["prompts"]:
        start_of_paragraph = d["paragraph"][:25]
        prompt_name = f"{start_of_paragraph}..."

        if "prompt name" not in d:
            d["prompt name"] = prompt_name
        else:
            d["prompt name"] = prompt_name

    with open("prompts.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)

add_length_types()
add_prompt_names()