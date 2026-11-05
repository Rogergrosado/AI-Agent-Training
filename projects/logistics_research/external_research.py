import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

OPENALEX_URL = "https://api.openalex.org/works"


def search_external_sources(query, max_results=3):
    """Search public research sources using OpenAlex."""

    if not isinstance(query, str) or not query.strip():
        raise ValueError("Research query must be a non-empty string")

    if not isinstance(max_results, int) or not 1 <= max_results <= 10:
        raise ValueError("max_results must be between 1 and 10")

    parameters = urlencode(
        {
            "search": query.strip(),
            "per-page": max_results,
        }
    )

    request = Request(
        f"{OPENALEX_URL}?{parameters}",
        headers={
            "User-Agent": "AI-Agent-Training/1.0",
            "Accept": "application/json",
        },
    )

    try:
        with urlopen(request, timeout=15) as response:
            payload = json.load(response)

    except (HTTPError, URLError, TimeoutError, OSError) as error:
        return {
            "query": query,
            "status": "error",
            "results": [],
            "error": str(error),
        }

    results = []

    for item in payload.get("results", []):
        location = item.get("primary_location") or {}
        source = location.get("source") or {}

        results.append(
            {
                "title": item.get("display_name"),
                "url": item.get("doi") or item.get("id"),
                "source": source.get("display_name"),
                "publication_date": item.get("publication_date"),
                "evidence_type": "research_metadata",
            }
        )

    return {
        "query": query,
        "status": "success",
        "results": results,
        "error": None,
    }


if __name__ == "__main__":
    query = "port congestion supply chain shipping delays"

    response = search_external_sources(query)

    print("=== Exercise 014: External Research ===")
    print(json.dumps(response, indent=2, ensure_ascii=False))
