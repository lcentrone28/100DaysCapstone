import requests
import json
import pypdf
import io
import re

def fetch_pdf_verses():
    pdf_url = "https://followtherabbi.com/wp-content/uploads/2020/06/365_Bible_Verses1.pdf"
    verses = []

    print("downloading pdf")
    headers = {

        'User-Agent': 'Utility Tools, Verse of The Day'

    }

    try:
        response = requests.get(pdf_url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"failed to download: {response.status_code}")
            return []

        pdf_file = io.BytesIO(response.content)
        reader = pypdf.PdfReader(pdf_file)

        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"

        full_text = full_text.replace("“", '"').replace("”", '"')
        full_text = full_text.replace("‘", "'").replace("’", "'")
        full_text = full_text.replace("—", "-")
        full_text = re.sub(r"Page \d+.*?PEACE CHURCH.*?\d+", "", full_text, flags=re.IGNORECASE)
        full_text = re.sub(r'\s+', ' ', full_text)

        pattern = r"(\d+)\.\s+(.*?)(?=\s+\d+\.\s+|$)"
        matches = re.findall(pattern, full_text)

        for verse_num, content in matches:
            content = content.strip()

            ref_match = re.search(r"^([\d\s]*[A-Za-z\s]+ \d+:\d+(-\d+)?)", content)
            if ref_match:
                verse = ref_match.group(1).strip()
                text = content[len(verse):].strip()
            else:
                verse = f"verse #{verse_num}"
                text = content

            if text:
                verse_data = {
                    "day": int(verse_num),
                    "text": text,
                    "verse": verse
                }
                verses.append(verse_data)

    except Exception as e:
        print(f"error: {e}")

    return verses

def create_json(list_name, data_list):
    json_structure = {
        list_name: data_list
    }
    with open("verses.json", "w", encoding="utf-8") as json_file:
        json.dump(json_structure, json_file, indent=4, ensure_ascii=False)

verses = fetch_pdf_verses()

if verses:
    verses.sort(key=lambda x: x["day"])
    create_json("verses", verses)