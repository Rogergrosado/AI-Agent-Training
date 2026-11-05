from urllib.parse import urlparse


def evaluate_evidence(source: dict, research_query: str) -> dict:
    """Evaluate research metadata without claiming content verification."""

    if not isinstance(source, dict):
        raise ValueError("Source must be a dictionary")

    if not isinstance(research_query, str):
        raise ValueError("Research query must be a string")

    title = source.get("title")
    url = source.get("url")
    publisher = source.get("source")

    title = title.strip() if isinstance(title, str) else ""
    url = url.strip() if isinstance(url, str) else ""
    publisher = publisher.strip() if isinstance(publisher, str) else ""

    parsed_url = urlparse(url)

    valid_url = parsed_url.scheme in {"http", "https"} and bool(parsed_url.hostname)

    traceable = bool(title and publisher and valid_url)

    query_terms = {
        word.lower().strip(".,:;!?")
        for word in research_query.split()
        if len(word.strip(".,:;!?")) >= 4
    }

    title_terms = {word.lower().strip(".,:;!?") for word in title.split()}

    overlap = query_terms.intersection(title_terms)

    relevance = "related" if overlap else "not_established"

    return {
        "title": title,
        "url": url,
        "source": publisher,
        "relevance": relevance,
        "traceable": traceable,
        "content_verified": False,
        "supports_specific_shipment_claim": False,
        "matching_terms": sorted(overlap),
        "evidence_limitations": (
            "Metadata only; full publication content has not been verified."
        ),
    }


if __name__ == "__main__":
    example_source = {
        "title": "Supply Chains and Port Congestion Around the World",
        "url": "https://doi.org/10.5089/9798400202957.001",
        "source": "IMF Working Papers",
    }

    example_query = "port congestion supply chain shipping delays"

    import json

    result = evaluate_evidence(example_source, example_query)

    print("=== Exercise 014: Evidence Quality Assessment ===")
    print(json.dumps(result, indent=2))
