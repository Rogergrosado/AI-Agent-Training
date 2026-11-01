"""
Exercise 008 - Logistics Web Search

Independent research module for packaging and handling symbols.

This module:
- Searches public web results.
- Preserves titles, URLs, and snippets.
- Saves research results as JSON.
- Does not change the visual recognition agent.
- Does not treat search snippets as verified compliance rules.
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from ddgs import DDGS

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR.parent / "results" / "exercise_008"

SEARCH_QUERIES = {
    "this way up": "ISO 780 this way up packaging handling symbol meaning",
    "keep dry": "ISO 780 keep dry umbrella packaging symbol meaning",
    "fragile": "ISO 780 fragile handle with care packaging symbol",
    "recyclable": "Mobius loop recycling symbol packaging meaning official",
    "dispose properly": "tidyman dispose properly packaging symbol meaning",
    "snowflake": "snowflake packaging symbol temperature meaning",
    "temperature": "ISO 780 temperature limits packaging symbol",
    "stacking limit": "ISO 780 stacking limit by number packaging symbol",
}

ALIASES = {
    "arrows": "this way up",
    "upward arrows": "this way up",
    "two upward arrows": "this way up",
    "umbrella": "keep dry",
    "broken glass": "fragile",
    "recycling": "recyclable",
    "recycling symbol": "recyclable",
    "trash can": "dispose properly",
    "trash can symbol": "dispose properly",
    "trash disposal": "dispose properly",
    "waste disposal": "dispose properly",
    "thermometer": "temperature",
    "snowflake symbol": "snowflake",
    "stacking": "stacking limit",
    "number 2": "number 2",
}


def normalize_symbol(symbol: str) -> str:
    """Normalize common visual labels for research lookup."""
    key = re.sub(r"\s+", " ", symbol.strip().casefold())
    key = key.replace("_", " ").replace("-", " ")
    return ALIASES.get(key, key)


def build_query(symbol: str) -> str:
    """Create a search query without assuming a symbol's meaning."""
    normalized = normalize_symbol(symbol)

    if normalized == "number 2" or normalized.isdigit():
        return "number 2 marking on shipping carton packaging meaning"

    return SEARCH_QUERIES.get(
        normalized,
        f"{normalized} packaging marking meaning logistics",
    )


def valid_public_url(url: str) -> bool:
    """Accept ordinary public HTTP(S) URLs only."""
    try:
        parsed = urlparse(url)
        hostname = (parsed.hostname or "").lower()

        if parsed.scheme not in {"http", "https"}:
            return False

        if not hostname or "." not in hostname:
            return False

        if hostname == "localhost" or hostname.endswith(".local"):
            return False

        if hostname.endswith(".internal"):
            return False

        return True

    except ValueError:
        return False


def search_symbol(symbol: str, max_results: int = 5) -> dict:
    """
    Search public web results for one symbol.

    Results are research leads, not independently verified facts.
    """
    query = build_query(symbol)

    record = {
        "symbol": symbol,
        "normalized_symbol": normalize_symbol(symbol),
        "query": query,
        "status": "not_searched",
        "sources": [],
        "warning": None,
    }

    try:
        with DDGS(timeout=20) as client:
            results = list(
                client.text(
                    query,
                    max_results=max_results,
                )
            )

        seen_urls = set()

        for result in results:
            title = str(result.get("title", "")).strip()
            url = str(result.get("href", "")).strip()
            snippet = str(result.get("body", "")).strip()

            if not valid_public_url(url):
                continue

            if url in seen_urls:
                continue

            seen_urls.add(url)

            record["sources"].append(
                {
                    "title": title,
                    "url": url,
                    "snippet": snippet,
                    "verification_status": "search_result_only",
                }
            )

        record["status"] = "results_found" if record["sources"] else "no_results"

        if not record["sources"]:
            record["warning"] = "No usable search results were returned."

    except Exception as error:
        record["status"] = "search_error"
        record["warning"] = f"{type(error).__name__}: {error}"

    return record


def research_symbols(symbols: list[str]) -> dict:
    """Research each unique symbol and collect the results."""
    unique_symbols = []
    seen = set()

    for symbol in symbols:
        normalized = normalize_symbol(symbol)

        if normalized not in seen:
            seen.add(normalized)
            unique_symbols.append(symbol)

    findings = []

    for index, symbol in enumerate(unique_symbols, 1):
        print(f"[{index}/{len(unique_symbols)}] " f"Researching: {symbol}")

        findings.append(search_symbol(symbol))

    return {
        "exercise": "008",
        "module": "logistics_web_search",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "research_status": "preliminary",
        "symbols_researched": len(unique_symbols),
        "findings": findings,
        "limitations": [
            "Search results are not verified source documents.",
            "A search snippet does not establish regulatory compliance.",
            "Visual detections remain unverified.",
            "Symbol meaning depends on context and applicable standards.",
            "Human verification is required before operational decisions.",
        ],
    }


def save_research(data: dict) -> Path:
    """Save the research results without overwriting prior runs."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")

    output_path = RESULTS_DIR / f"web_research_{timestamp}.json"

    output_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return output_path


def print_report(data: dict) -> None:
    """Display a readable research summary."""
    print("\n" + "=" * 60)
    print("EXERCISE 008 - LOGISTICS WEB RESEARCH")
    print("=" * 60)

    for finding in data["findings"]:
        print(f"\nSymbol: {finding['symbol']}")
        print(f"Query: {finding['query']}")
        print(f"Status: {finding['status']}")

        if finding["warning"]:
            print(f"Warning: {finding['warning']}")

        for index, source in enumerate(finding["sources"], 1):
            print(f"\n  Source {index}: {source['title']}")
            print(f"  URL: {source['url']}")
            print(f"  Snippet: {source['snippet'][:250]}")

    print("\n" + "=" * 60)
    print("RESEARCH LIMITATIONS")
    print("=" * 60)

    for limitation in data["limitations"]:
        print(f"- {limitation}")


def main() -> None:
    print("\nEXERCISE 008 - LOGISTICS WEB SEARCH")
    print("Independent module test\n")

    symbols = [
        "This Way Up",
        "Recycling",
        "Dispose Properly",
        "Keep Dry",
        "Fragile",
        "Snowflake",
    ]

    print("Researching six reference symbol labels.")
    print("Internet connection required.\n")

    data = research_symbols(symbols)

    output_path = save_research(data)

    print_report(data)

    print(f"\nResearch JSON saved to: {output_path}")
    print("\nWeb research test completed.")


if __name__ == "__main__":
    main()
