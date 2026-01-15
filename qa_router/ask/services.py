import csv
import json
from pathlib import Path

GEO_KEYWORDS = {
    "soil": 2, "flood": 2, "bodem": 2, "overstroming": 2,
    "location": 1, "zone": 1, "area": 1, "map": 1,
    "kaart": 1, "gebied": 1, "natuur": 1, "water": 1
}

REGULATION_KEYWORDS = {
    "regulation": 3, "rule": 2, "article": 2, "law": 2,
    "permit": 2, "requirement": 2, "allowed": 2, "forbidden": 2,
    "artikel": 2, "voorschrift": 2, "vergunning": 2,
    "building": 1
}

BASE_DIR = Path(__file__).resolve().parents[1]


def determine_source(question: str) -> str:
    question_lower = question.lower()

    geo_score = sum(weight for kw, weight in GEO_KEYWORDS.items() if kw in question_lower)
    reg_score = sum(weight for kw, weight in REGULATION_KEYWORDS.items() if kw in question_lower)

    if geo_score > reg_score:
        return "geo"
    elif reg_score > geo_score:
        return "regulation"
    else:
        return "unknown"

def search_geo_data(question: str) -> str:
    question_lower = question.lower()
    results = []

    with open(BASE_DIR / "data" / "mock_geo_data.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["name"].lower() in question_lower or \
                    any(word in row["name"].lower() for word in question_lower.split()):
                if row["status"] == "1" and row["api_name"]:
                    results.append({
                        "name": row["name"],
                        "data": json.loads(row["api_name"])
                    })

    if results:
        return f"Found {len(results)} result(s): {json.dumps(results[:3], indent=2)}"
    return "No matching geo data found."


def search_regulation_data(question: str) -> str:
    question_lower = question.lower()

    with open(BASE_DIR / "data" / "mock_regulation_data.txt", "r", encoding="utf-8") as f:
        content = f.read()

    articles = content.split("Art.")
    matching = []

    for article in articles:
        if any(word in article.lower() for word in question_lower.split() if len(word) > 3):
            matching.append("Art." + article[:300].strip())

    if matching:
        return f"Found {len(matching)} relevant article(s):\n\n" + "\n\n".join(matching[:2])
    return "No matching regulations found."


def process_question(question: str) -> dict:
    source = determine_source(question)

    if source == "geo":
        answer = search_geo_data(question)
    elif source == "regulation":
        answer = search_regulation_data(question)
    else:
        answer = "I couldn't determine which data source to use. Please ask about geographic data (soil, floods, zones) or regulations (building rules, permits, articles)."

    return {
        "answer": answer,
        "source": source
    }

