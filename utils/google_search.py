import requests

GOOGLE_API_KEY = "GOOGLE_API_KEY"   # Replace with your actual API key
GOOGLE_CSE_ID = "GOOGLE_CSE_ID"     # Replace with your actual Custom Search Engine ID

def google_search(query, max_results=10):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": query,
        "num": max_results
    }

    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()

        items = data.get("items", [])
        results = []

        for item in items:
            title = item.get("title")
            link = item.get("link")
            snippet = item.get("snippet", "")
            results.append({
                "title": title,
                "link": link,
                "description": snippet
            })

        return results

    except Exception as e:
        print("Google Search API Error:", e)
        return []
