import json, time
import httpx
import mwparserfromhell
from app.config import WIKI_API, USER_AGENT, CORPUS_PATH, DATA_DIR

def fetch_wiki_text(client: httpx.Client, title: str) -> str:
    resp = client.get(WIKI_API, params={
        "action": "parse",
        "page": title,
        "prop": "wikitext",
        "format": "json",
        "redirects": 1,
    })
    resp.raise_for_status()
    return resp.json()["parse"]["wikitext"]["*"]

def to_snippets(title: str, wiki_text: str) -> list[dict]:
    text = mwparserfromhell.parse(wiki_text).strip_code()
    snippets = []
    for para in text.split("\n\n"):
        para = " ".join(para.split())
        if len(para) < 80:
            continue
        snippets.append({"source": title, "text": para})
    return snippets

def category_titles(client, category: str) -> list[str]:
    titles, cont = [], None
    while True:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": f"Category:{category}",
            "cmlimit": 500,
            "cmtype": "page",
            "format": "json",
        }
        if cont:
            params["cmcontinue"] = cont
        data = client.get(WIKI_API, params=params).json()
        titles += [m["title"] for m in data["query"]["categorymembers"]]
        cont = data.get("continue", {}).get("cmcontinue")
        if not cont:
            return titles

CATEGORIES = [
    "Straw Hat Pirates Members",
    "Marine Officers",
    "Four Emperors",
    "Devil Fruits",
    "Islands",
    "Ships",
]

def main() -> None:

    corpus: list[dict] = []
    seen: set[str] = set()

    headers = {"User-Agent": USER_AGENT}

    with httpx.Client(headers=headers, timeout=30) as client:
        titles = []
        for cat in CATEGORIES:
            titles += category_titles(client, cat)
        for title in titles:
            if title in seen:
                continue
            seen.add(title)
            try:
                wikitext = fetch_wiki_text(client, title)
            except Exception as e:
                print(f"Error fetching {title}: {e}")
                continue
            corpus += to_snippets(title, wikitext)
            time.sleep(1)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CORPUS_PATH.write_text(json.dumps(corpus, indent=2, ensure_ascii=False))
    print(f"Saved {len(corpus)} snippets to {CORPUS_PATH}")

if __name__ == "__main__":
    main()
