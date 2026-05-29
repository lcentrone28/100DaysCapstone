import requests
import json
import time

def fetch_wiki_prompts(target_count, max_batches):
    url = "https://en.wikipedia.org/w/api.php"
    paragraphs = []
    batch_number = 0

    headers = {

        'User-Agent': 'Utility Tools, Typing Test'
    }

    params = {
        "action": "query",
        "format": "json",
        "generator": "random",
        "grnnamespace": 0,
        "prop": "extracts",
        "exintro": False,
        "explaintext": True,
        "grnlimit": 50
    }

    while len(paragraphs) < target_count and batch_number < max_batches:
        batch_number += 1
        print(f"requesting batch #{batch_number}, retrieved {len(paragraphs)} paragraphs so far")

        try:
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 429:
                print("hit rate limit")

            if response.status_code != 200:
                time.sleep(5)
                continue

            data = response.json()
            pages = data.get("query", {}).get("pages", {})

            if not pages:
                time.sleep(5)
                continue

            for page_id, page_info in pages.items():
                text = page_info.get("extract", "").strip()

                text = text.replace("\n", " ")
                text = text.replace("“", '"').replace("”", '"')
                text = text.replace("‘", "'").replace("’", "'")
                text = text.replace("—", "-")

                if len(text) > 200 and "may refer to:" not in text and text.isascii():
                    paragraph_data = {
                        "paragraph": text,
                        "length": len(text)
                    }
                    paragraphs.append(paragraph_data)

                    if len(paragraphs) == target_count:
                        break

            time.sleep(1.0)

        except Exception as e:
            print(f"error: {e}")
            time.sleep(2)

    return paragraphs

def create_json(list_name, data_list):
    json_structure = {
        list_name: data_list
    }
    with open("prompts.json", "w", encoding="utf-8") as json_file:
        json.dump(json_structure, json_file, indent=4)

prompts = fetch_wiki_prompts(target_count=100, max_batches=11)

if prompts:
    create_json("prompts", prompts)