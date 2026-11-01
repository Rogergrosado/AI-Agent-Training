import json
from datetime import datetime, timezone
from pathlib import Path
from logistics_web_search import research_symbols, save_research

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR.parent / "results" / "exercise_008"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize_label(label):
    return " ".join(str(label).lower().strip().split())


def get_search_records(data):
    """
    Locate research records without assuming a single JSON schema.
    """
    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        for key in ("findings", "results", "research", "search_results", "symbols"):
            records = data.get(key)
            if isinstance(records, list):
                return records

    return []


def integrate(visual_data, web_data):
    analysis = visual_data.get("analysis", {})
    visual_symbols = analysis.get("symbols", [])
    search_records = get_search_records(web_data)

    integrated_symbols = []

    for item in visual_symbols:
        if not isinstance(item, dict):
            continue

        symbol_name = str(item.get("symbol", "Unknown"))
        matched_research = []

        for record in search_records:
            if not isinstance(record, dict):
                continue

            research_name = str(record.get("symbol", record.get("label", "")))

            if normalize_label(research_name) == normalize_label(symbol_name):
                matched_research.append(record)

        integrated_symbols.append(
            {
                "symbol": symbol_name,
                "visual_evidence": item.get("visual_evidence", ""),
                "location": item.get("location", ""),
                "model_confidence": item.get("confidence", "unknown"),
                "visual_interpretation": item.get("possible_interpretation", "Unknown"),
                "research_matches": matched_research,
                "research_status": (
                    "results_found"
                    if any(
                        record.get("status") == "results_found"
                        and record.get("sources")
                        for record in matched_research
                    )
                    else (
                        "search_error"
                        if any(
                            record.get("status") == "search_error"
                            for record in matched_research
                        )
                        else "no_results" if matched_research else "not_matched"
                    )
                ),
                "verification_status": "human_review_required",
            }
        )

    return {
        "exercise": "008",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "image_path": visual_data.get("image_path", ""),
        "visual_symbol_count": len(integrated_symbols),
        "matched_symbol_count": sum(
            bool(item["research_matches"]) for item in integrated_symbols
        ),
        "successful_research_count": sum(
            item["research_status"] == "results_found" for item in integrated_symbols
        ),
        "symbols": integrated_symbols,
        "limitations": [
            "Search results are not independently verified.",
            "Matching labels does not prove visual recognition accuracy.",
            "Search snippets do not establish regulatory compliance.",
            "All operational recommendations require human verification.",
        ],
    }


def main():
    print("\nEXERCISE 008 - VISUAL + WEB INTEGRATION")
    print("=" * 55)

    visual_path = input("\nEnter saved visual analysis JSON path: ").strip().strip('"')

    print("\nLoading visual analysis...")

    if not Path(visual_path).is_file():
        print("\nERROR: Visual JSON not found.")
        return

    try:
        visual_data = load_json(visual_path)

        visual_symbols = visual_data.get("analysis", {}).get("symbols", [])

        if not isinstance(visual_symbols, list):
            print("\nERROR: Invalid visual symbols list.")
            return

        symbol_names = [
            str(item["symbol"])
            for item in visual_symbols
            if isinstance(item, dict) and item.get("symbol")
        ]

        if not symbol_names:
            print("\nERROR: No visual symbols available for research.")
            return

        print(f"\nDetected symbols: {len(symbol_names)}")
        print("Starting automatic web research...\n")

        web_data = research_symbols(symbol_names)

        web_path = save_research(web_data)

        print(f"\nResearch JSON saved to: {web_path}")

        result = integrate(visual_data, web_data)

    except (OSError, ValueError, TypeError, AttributeError, KeyError) as error:
        print(f"\nERROR: {type(error).__name__}: {error}")
        return

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    output_path = RESULTS_DIR / f"integrated_report_{timestamp}.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=2, ensure_ascii=False)

    print("\nINTEGRATION SUMMARY")
    print("=" * 55)
    print(f"Visual symbols: {result['visual_symbol_count']}")
    print(f"Research records matched: {result['matched_symbol_count']}")
    print(f"Successful research: {result['successful_research_count']}")

    for symbol in result["symbols"]:
        print(f"- {symbol['symbol']}: " f"{symbol['research_status']}")

    print(f"\nReport saved to: {output_path}")
    print("\nIntegration completed.")


if __name__ == "__main__":
    main()
