"""Exercise 008 - Visual Logistics Evaluator.

Compare model predictions with a human-reviewed ground truth.
Strict and alias-aware scores are retained for comparison.

Important: This evaluator does not independently verify image pixels,
symbol occurrence counts, operational meanings, or model confidence.
"""

from __future__ import annotations
from datetime import datetime, timezone

import json
import re
from pathlib import Path

from multimodal_logistics_agent import analyze_shipping_image

BASE_DIR = Path(__file__).resolve().parent

DEFAULT_GROUND_TRUTH = BASE_DIR / "exercise_008_generic_ground_truth.json"


ALIASES = {
    "recycling symbol": "recyclable",
    "recycling": "recyclable",
    "recycle": "recyclable",
    "recyclable material": "recyclable",
    "trash symbol": "dispose properly",
    "trash can symbol": "dispose properly",
    "waste disposal": "dispose properly",
    "trash disposal": "dispose properly",
    "umbrella": "keep dry",
    "umbrella symbol": "keep dry",
    "glass": "fragile",
    "wine glass": "fragile",
    "fragile glass": "fragile",
    "upright arrows": "this way up",
    "upward arrows": "this way up",
    "two upward arrows": "this way up",
    "snowflake symbol": "snowflake",
}


AMBIGUOUS_LABELS = {
    "temperature symbol",
    "temperature control",
    "temperature range",
    "cold symbol",
    "handling symbol",
}

BRANDS = {"amazon", "fedex", "dhl", "walmart"}

RESULTS_DIR = BASE_DIR.parent / "results" / "exercise_008"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def save_analysis(analysis: dict, image_path: Path) -> Path:
    """Save the model response for reproducible evaluation."""

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    output_path = RESULTS_DIR / f"visual_analysis_{timestamp}.json"

    record = {
        "exercise": "008",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "image_path": str(image_path.resolve()),
        "analysis": analysis,
    }

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(record, file, indent=2, ensure_ascii=False)

    return output_path


def normalize(value: object) -> str:
    return " ".join(str(value).casefold().replace("_", " ").split())


def canonical(value: object, alias_aware: bool) -> str:
    name = normalize(value)
    return ALIASES.get(name, name) if alias_aware else name


def calculate_metrics(
    expected: list[str],
    predicted: list[str],
    alias_aware: bool = False,
) -> dict:
    expected_set = {canonical(name, alias_aware) for name in expected}
    predicted_set = {canonical(name, alias_aware) for name in predicted}

    matched = expected_set & predicted_set
    unexpected = predicted_set - expected_set
    missed = expected_set - predicted_set

    tp = len(matched)
    fp = len(unexpected)
    fn = len(missed)

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0

    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "matched": sorted(matched),
        "unexpected": sorted(unexpected),
        "missed": sorted(missed),
    }


def print_metrics(title: str, result: dict) -> None:
    print(f"\n{title}")
    print("-" * len(title))

    print(f"True positives:  {result['tp']}")
    print(f"False positives: {result['fp']}")
    print(f"False negatives: {result['fn']}")
    print(f"Precision:       {result['precision']:.2%}")
    print(f"Recall:          {result['recall']:.2%}")
    print(f"F1 Score:        {result['f1']:.2%}")

    print(f"Matched:    {result['matched']}")
    print(f"Unexpected: {result['unexpected']}")
    print(f"Missed:     {result['missed']}")


def load_ground_truth(path: Path) -> dict:
    with path.open("r", encoding="utf-8-sig") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("Ground truth must be a JSON object.")

    expected = data.get("expected_symbols")

    if not isinstance(expected, list):
        raise ValueError("Ground truth must contain expected_symbols.")

    if not all(isinstance(item, str) for item in expected):
        raise ValueError("Every expected symbol must be a string.")

    return data


def get_other_markings(ground_truth: dict) -> set[str]:
    markings = set()

    for item in ground_truth.get("other_markings", []):
        if isinstance(item, str):
            markings.add(normalize(item))

        elif isinstance(item, dict):
            markings.add(normalize(item.get("marking", "")))

    return markings


def classify_label(
    label: str,
    known_markings: set[str],
) -> str:
    name = normalize(label)

    if (
        name in known_markings
        or re.fullmatch(r"\d+(?:[.,]\d+)?", name)
        or "logo" in name
        or name in BRANDS
    ):
        return "OTHER MARKING"

    if name in AMBIGUOUS_LABELS:
        return "AMBIGUOUS"

    return "HANDLING CANDIDATE"


def review_semantics(
    entries: list[dict],
    known_markings: set[str],
) -> list[str]:
    warnings = []

    for entry in entries:
        name = str(entry.get("symbol", ""))
        meaning = str(entry.get("meaning", ""))
        action = str(entry.get("action", ""))

        category = classify_label(name, known_markings)
        description = normalize(f"{meaning} {action}")

        if category == "OTHER MARKING":
            unsupported_terms = (
                "series",
                "stacking capacity",
                "set of",
                "flammable",
                "temperature",
            )

            if any(term in description for term in unsupported_terms):
                warnings.append(
                    f"{name}: possible unsupported interpretation "
                    "of a non-handling marking."
                )

        if category == "AMBIGUOUS":
            warnings.append(f"{name}: exact symbol meaning is unverified.")

        if "temperature" in normalize(name) or "temperature" in description:
            if re.search(
                r"-?\d+\s*(?:°|degrees?)?\s*c\b",
                description,
            ):
                warnings.append(
                    f"{name}: numerical temperature claim "
                    "requires visual verification."
                )

    return warnings


def main() -> None:
    print("=" * 60)
    print("EXERCISE 008 - VISUAL LOGISTICS EVALUATOR")
    print("=" * 60)

    ground_truth_input = (
        input("\nGround truth JSON " f"[Enter for {DEFAULT_GROUND_TRUTH.name}]: ")
        .strip()
        .strip('"')
        .strip("'")
    )

    ground_truth_path = (
        Path(ground_truth_input).expanduser()
        if ground_truth_input
        else DEFAULT_GROUND_TRUTH
    )

    try:
        ground_truth = load_ground_truth(ground_truth_path)

    except (
        OSError,
        UnicodeError,
        ValueError,
        json.JSONDecodeError,
    ) as error:
        print(f"\nERROR reading ground truth: {error}")
        return

    image_input = input("\nEnter image path: ").strip().strip('"').strip("'")

    if not image_input:
        print("\nERROR: An image path is required.")
        return

    image_path = Path(image_input).expanduser()

    if not image_path.is_file():
        print(f"\nERROR: Image not found: {image_path}")
        return

    print("\nPreparing visual logistics evaluation...")

    try:
        replay_input = (
            input("\nSaved analysis JSON path [Enter to run model]: ")
            .strip()
            .strip('"')
            .strip("'")
        )

        if replay_input:
            replay_path = Path(replay_input).expanduser()

            with replay_path.open("r", encoding="utf-8") as file:
                saved_record = json.load(file)

            analysis = saved_record["analysis"]

            print("\nREPLAY MODE: Using saved model predictions.")
            print("No new Ollama inference performed.")

        else:
            analysis = analyze_shipping_image(str(image_path))

            saved_path = save_analysis(analysis, image_path)

            print(f"\nModel response saved to: {saved_path}")

    except Exception as error:
        print(f"\nERROR during image analysis: " f"{type(error).__name__}: {error}")
        return

    if not isinstance(analysis, dict):
        print("\nERROR: Model returned an invalid analysis.")
        return

    raw_entries = analysis.get("symbols")

    if not isinstance(raw_entries, list):
        print("\nERROR: Model response has no symbols list.")
        return

    entries = [
        entry
        for entry in raw_entries
        if isinstance(entry, dict) and normalize(entry.get("symbol", ""))
    ]

    predicted = [str(entry["symbol"]) for entry in entries]

    expected = ground_truth["expected_symbols"]

    known_markings = get_other_markings(ground_truth)

    handling = []
    other_markings = []
    ambiguous = []

    for label in predicted:
        category = classify_label(label, known_markings)

        if category == "HANDLING CANDIDATE":
            handling.append(label)

        elif category == "OTHER MARKING":
            other_markings.append(label)

        else:
            ambiguous.append(label)

    print("=" * 60)
    print("VISUAL LABEL BENCHMARK")
    print("=" * 60)

    print(f"Expected unique labels: " f"{len({normalize(x) for x in expected})}")
    print(f"Predicted entries:       {len(predicted)}")
    print(f"Handling candidates:     {len(handling)}")
    print(f"Other markings:          {len(other_markings)}")
    print(f"Ambiguous labels:        {len(ambiguous)}")

    strict = calculate_metrics(
        expected,
        predicted,
        alias_aware=False,
    )

    alias_aware = calculate_metrics(
        expected,
        predicted,
        alias_aware=True,
    )

    handling_only = calculate_metrics(
        expected,
        handling,
        alias_aware=True,
    )

    print_metrics("STRICT LABEL MATCH", strict)

    print_metrics("ALIAS-AWARE LABEL MATCH", alias_aware)

    print_metrics(
        "HANDLING-ONLY ALIAS-AWARE (EXPLORATORY)",
        handling_only,
    )

    print("\n" + "=" * 60)
    print("OTHER MARKINGS AND AMBIGUOUS LABELS")
    print("=" * 60)

    print(f"Other markings: {other_markings}")
    print(f"Ambiguous labels: {ambiguous}")

    print(
        "\nThese classifications are provisional. "
        "They do not prove what is visible in the image."
    )

    print("\n" + "=" * 60)
    print("OCCURRENCE COUNT REVIEW")
    print("=" * 60)

    expected_counts = ground_truth.get("expected_symbol_occurrences")

    if isinstance(expected_counts, dict):
        print(f"Expected occurrences: {expected_counts}")
    else:
        print("No occurrence ground truth available.")

    print(
        "Status: NOT SCORED. The agent does not provide "
        "verified per-instance symbol detections."
    )

    print("\n" + "=" * 60)
    print("MEANING AND ACTION REVIEW")
    print("=" * 60)

    for entry in entries:
        print(f"\nSymbol: {entry.get('symbol', 'Unknown')}")
        print(f"Meaning: {entry.get('meaning', 'N/A')}")
        print(f"Action: {entry.get('action', 'N/A')}")
        print(f"Model confidence: " f"{entry.get('confidence', 'N/A')}")

    print("\n" + "=" * 60)
    print("SAFETY AND SEMANTIC WARNINGS")
    print("=" * 60)

    warnings = review_semantics(
        entries,
        known_markings,
    )

    if warnings:
        for warning in warnings:
            print(f"WARNING: {warning}")
    else:
        print("No rule-based warnings found. " "This is NOT a safety clearance.")

    print("\n" + "=" * 60)
    print("MODEL UNCERTAINTIES")
    print("=" * 60)

    uncertainties = analysis.get("uncertainties", [])

    if isinstance(uncertainties, list):
        if uncertainties:
            for uncertainty in uncertainties:
                print(f"- {uncertainty}")
        else:
            print("None reported.")
    else:
        print(uncertainties or "None reported.")

    print("\n" + "=" * 60)
    print("FINAL EVALUATION NOTES")
    print("=" * 60)

    print("1. Strict and alias-aware scores compare unique labels.")
    print("2. Alias matching does not improve visual recognition.")
    print("3. Excluding other markings changes score denominators.")
    print("4. Occurrence counts are not independently verified.")
    print("5. Meanings, actions, and temperature claims " "require human verification.")
    print("6. Model-reported confidence is not a calibrated " "accuracy measurement.")

    print("\nEvaluation completed.")


if __name__ == "__main__":
    main()
