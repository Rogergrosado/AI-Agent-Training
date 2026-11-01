import json
import re
from pathlib import Path

from ollama import chat, ResponseError

MODEL_NAME = "qwen2.5vl:3b"
SUPPORTED_FORMATS = {".png", ".jpg", ".jpeg", ".webp"}
CONFIDENCE_LEVELS = {"high", "medium", "low"}

UNKNOWN = "Unknown"
REVIEW_REQUIRED = "Human verification required."

MODEL_SCHEMA = {
    "type": "object",
    "properties": {
        "image_description": {"type": "string"},
        "symbols": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "visual_evidence": {"type": "string"},
                    "location": {"type": "string"},
                    "confidence": {
                        "type": "string",
                        "enum": ["high", "medium", "low"],
                    },
                },
                "required": [
                    "symbol",
                    "visual_evidence",
                    "location",
                    "confidence",
                ],
            },
        },
        "uncertainties": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": [
        "image_description",
        "symbols",
        "uncertainties",
    ],
}


def validate_image(image_path: str) -> Path:
    image = Path(image_path).expanduser()

    if not image.is_file():
        raise FileNotFoundError(f"Image not found: {image}")

    if image.suffix.lower() not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported image format: {image.suffix}")

    return image


def parse_model_json(content: str) -> dict:
    if not content or not content.strip():
        raise ValueError("Empty model response.")

    try:
        data = json.loads(content)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON at line {error.lineno}, "
            f"column {error.colno}: {error.msg}"
        ) from error

    if not isinstance(data, dict):
        raise ValueError("Model response must be a JSON object.")

    return data


def validate_model_response(data: dict) -> None:
    if not isinstance(data.get("image_description"), str):
        raise ValueError("Invalid image description.")

    if not isinstance(data.get("symbols"), list):
        raise ValueError("Invalid symbols list.")

    if not isinstance(data.get("uncertainties"), list):
        raise ValueError("Invalid uncertainties list.")

    if not all(isinstance(x, str) for x in data["uncertainties"]):
        raise ValueError("Uncertainties must contain strings.")

    required = {
        "symbol",
        "visual_evidence",
        "location",
        "confidence",
    }

    for index, item in enumerate(data["symbols"], 1):
        if not isinstance(item, dict):
            raise ValueError(f"Symbol {index} is not an object.")

        if not required.issubset(item):
            raise ValueError(f"Symbol {index} has missing fields.")

        for field in required:
            if not isinstance(item[field], str):
                raise ValueError(f"Symbol {index}: invalid {field}.")

        if item["confidence"] not in CONFIDENCE_LEVELS:
            raise ValueError(f"Symbol {index}: invalid confidence.")


def normalize_symbol(name: str) -> str:
    """
    Normalize equivalent label names.

    This does not verify whether a symbol is visible.
    The evaluator remains responsible for scoring.
    """
    key = re.sub(r"\s+", " ", name.casefold().strip())
    key = key.replace("_", " ").replace("-", " ")

    aliases = {
        "upward arrows": "this way up",
        "up arrows": "this way up",
        "two upward arrows": "this way up",
        "this side up": "this way up",
        "this way up symbol": "this way up",
        "umbrella": "keep dry",
        "umbrella symbol": "keep dry",
        "keep dry symbol": "keep dry",
        "fragile symbol": "fragile",
        "broken glass": "fragile",
        "broken glass symbol": "fragile",
        "recycling": "recyclable",
        "recycling symbol": "recyclable",
        "recycle symbol": "recyclable",
        "recyclable symbol": "recyclable",
        "mobius loop": "recyclable",
        "trash": "dispose properly",
        "trash symbol": "dispose properly",
        "trash can": "dispose properly",
        "trash can symbol": "dispose properly",
        "waste disposal": "dispose properly",
        "trash disposal": "dispose properly",
        "dispose properly symbol": "dispose properly",
        "snowflake symbol": "snowflake",
        "temperature symbol": "temperature",
        "thermometer symbol": "temperature",
        "stacking limit symbol": "stacking limit",
    }

    return aliases.get(key, key)


def classify_symbol(name: str) -> dict:
    """
    Provide cautious interpretations from detected names.
    These interpretations do not verify image pixels.
    """
    key = normalize_symbol(name)

    definitions = {
        "this way up": (
            "handling_symbol",
            "Possible package orientation marking.",
            "Keep the indicated side upright after verification.",
        ),
        "keep dry": (
            "handling_symbol",
            "Possible protection-from-moisture marking.",
            "Protect from moisture after verification.",
        ),
        "fragile": (
            "handling_symbol",
            "Possible fragile handling instruction.",
            "Handle carefully after verification.",
        ),
        "recyclable": (
            "handling_symbol",
            "Possible recycling-related marking.",
            REVIEW_REQUIRED,
        ),
        "dispose properly": (
            "other_marking",
            "Possible waste-disposal marking.",
            REVIEW_REQUIRED,
        ),
        "snowflake": (
            "handling_symbol",
            "Possible temperature-related marking; " "exact requirement unknown.",
            REVIEW_REQUIRED,
        ),
        "temperature": (
            "handling_symbol",
            "Possible temperature-related marking; " "exact requirement unknown.",
            REVIEW_REQUIRED,
        ),
        "stacking limit": (
            "handling_symbol",
            "Possible stacking-limit marking; " "exact limit unverified.",
            REVIEW_REQUIRED,
        ),
    }

    if key in definitions:
        category, interpretation, action = definitions[key]

    elif key.isdigit() or key.startswith("number "):
        category = "other_marking"
        interpretation = "Numeric marking; exact meaning unverified."
        action = REVIEW_REQUIRED

    elif "logo" in key:
        category = "brand_logo"
        interpretation = "Possible brand or company marking."
        action = REVIEW_REQUIRED

    else:
        category = "unknown"
        interpretation = UNKNOWN
        action = REVIEW_REQUIRED

    return {
        "category": category,
        "possible_interpretation": interpretation,
        "meaning": UNKNOWN,
        "recommended_action": action,
        "verification_status": "human_review_required",
    }


def expand_analysis(data: dict) -> dict:
    expanded = []

    for item in data["symbols"]:
        details = classify_symbol(item["symbol"])

        expanded.append(
            {
                "symbol": item["symbol"],
                "visual_evidence": item["visual_evidence"],
                "location": item["location"],
                "category": details["category"],
                "possible_interpretation": details["possible_interpretation"],
                "meaning": details["meaning"],
                "recommended_action": details["recommended_action"],
                "verification_status": details["verification_status"],
                "confidence": item["confidence"],
            }
        )

    return {
        "image_description": data["image_description"],
        "symbols": expanded,
        "uncertainties": data["uncertainties"],
    }


def validate_analysis(data: dict) -> None:
    if not isinstance(data, dict):
        raise ValueError("Analysis must be an object.")

    if not isinstance(data.get("image_description"), str):
        raise ValueError("Missing image description.")

    if not isinstance(data.get("symbols"), list):
        raise ValueError("Missing symbols list.")

    if not isinstance(data.get("uncertainties"), list):
        raise ValueError("Missing uncertainties list.")

    required = {
        "symbol",
        "visual_evidence",
        "location",
        "category",
        "possible_interpretation",
        "meaning",
        "recommended_action",
        "verification_status",
        "confidence",
    }

    for index, item in enumerate(data["symbols"], 1):
        if not isinstance(item, dict):
            raise ValueError(f"Marking {index} is not an object.")

        if not required.issubset(item):
            raise ValueError(f"Marking {index} has missing fields.")

        if any(not isinstance(item[field], str) for field in required):
            raise ValueError(f"Marking {index} has invalid field types.")

        if item["confidence"] not in CONFIDENCE_LEVELS:
            raise ValueError(f"Marking {index}: invalid confidence.")

        if item["category"] not in {
            "handling_symbol",
            "other_marking",
            "brand_logo",
            "unknown",
        }:
            raise ValueError(f"Marking {index}: invalid category.")

        if item["verification_status"] not in {
            "provisional",
            "human_review_required",
        }:
            raise ValueError(f"Marking {index}: invalid verification.")


def review_analysis_quality(data: dict) -> dict:
    warnings = []
    seen = set()

    for index, item in enumerate(data["symbols"], 1):
        name = item["symbol"].strip()
        evidence = item["visual_evidence"].strip()
        location = item["location"].strip()

        if not name:
            warnings.append(f"Marking {index}: missing name.")

        if not evidence or evidence.casefold() in {"unknown", "none", "n/a"}:
            warnings.append(f"Marking {index}: weak visual evidence.")

        if not location or location.casefold() in {"unknown", "none", "n/a"}:
            warnings.append(f"Marking {index}: unclear location.")

        key = (normalize_symbol(name), location.casefold())

        if key in seen:
            warnings.append(f"Marking {index}: possible duplicate.")

        seen.add(key)

    data["quality_warnings"] = warnings
    return data


def apply_safety_rules(data: dict) -> dict:
    for item in data["symbols"]:
        key = normalize_symbol(item["symbol"])

        if key.isdigit() or key.startswith("number "):
            item["category"] = "other_marking"
            item["meaning"] = UNKNOWN
            item["possible_interpretation"] = (
                "Numeric marking; exact meaning unverified."
            )

        if key in {"snowflake", "temperature"}:
            item["meaning"] = UNKNOWN
            item["possible_interpretation"] = (
                "Possible temperature-related marking; " "exact requirement unknown."
            )

        item["verification_status"] = "human_review_required"
        item["recommended_action"] = REVIEW_REQUIRED

    return data


def analyze_shipping_image(image_path: str) -> dict:
    """Analyze one image with a local vision model."""

    image = validate_image(image_path)

    prompt = """
You are a logistics visual inspection assistant.

Carefully inspect the entire supplied image before answering.
Your task is to recognize visible packaging markings, not
to certify shipping compliance.

Examine each visible package separately, scanning from top
to bottom and left to right.

Pay particular attention to small printed icons and markings.

Look for visual features such as:
- Arrows indicating package orientation
- Umbrellas or rain-protection icons
- Broken glass or fragile markings
- Recycling loops and recycling-related markings
- Waste-disposal icons
- Snowflakes, thermometers, or temperature-related icons
- Numbers and possible stacking-related markings
- Other distinct visible symbols

These are examples of visual features to inspect, NOT a list
of symbols that must appear. Do not report an example unless
you can identify supporting evidence in the image.

For every distinct visible marking provide:
- symbol: a short, conventional English name
- visual_evidence: what its shape actually looks like
- location: approximate position or package
- confidence: high, medium, or low

Recognition rules:
1. Use the clearest conventional name supported by the image.
2. Describe visual evidence rather than repeating the label.
3. Do not confuse upward arrows with downward arrows.
4. Do not confuse recycling with waste-disposal markings.
5. Do not assume that a number represents a stacking limit.
6. Do not infer an exact temperature from a snowflake alone.
7. Do not invent package contents, weights, or hazards.
8. Include partially visible markings only when identifiable;
   otherwise report them as uncertainties.
9. Report distinct markings without unnecessary repetition.
10. Do not invent markings to reach a target count.
11. Keep descriptions short and factual.
12. Do not explain meanings or operational recommendations.

Return only a compact JSON object matching the supplied schema.
No Markdown, commentary, or text outside JSON.
"""

    last_error = None

    for attempt in range(1, 3):
        print(f"Model attempt {attempt}/2...")

        try:
            response = chat(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                        "images": [str(image)],
                    }
                ],
                format=MODEL_SCHEMA,
                options={
                    "num_ctx": 4096,
                    "num_predict": 2048,
                    "temperature": 0,
                },
            )

            compact_data = parse_model_json(response.message.content)
            validate_model_response(compact_data)

            data = expand_analysis(compact_data)
            validate_analysis(data)

            data = review_analysis_quality(data)
            data = apply_safety_rules(data)
            data["model_attempts"] = attempt

            return data

        except ValueError as error:
            last_error = error
            print(f"Attempt {attempt} failed: {error}")

    raise ValueError(
        "Both attempts failed to produce valid structured data. "
        f"Last error: {last_error}"
    )


def print_report(data: dict) -> None:
    print("\n" + "=" * 60)
    print("MULTIMODAL LOGISTICS INSPECTION REPORT")
    print("=" * 60)

    print(f"\nImage: {data['image_description']}")
    print(f"Markings detected: {len(data['symbols'])}")
    print(f"Model attempts: {data.get('model_attempts', 'N/A')}")

    for index, item in enumerate(data["symbols"], 1):
        print("\n" + "-" * 60)
        print(f"{index}. {item['symbol']}")
        print(f"   Evidence: {item['visual_evidence']}")
        print(f"   Location: {item['location']}")
        print(f"   Category: {item['category']}")
        print("   Possible interpretation: " f"{item['possible_interpretation']}")
        print(f"   Meaning: {item['meaning']}")
        print(f"   Action: {item['recommended_action']}")
        print(f"   Verification: {item['verification_status']}")
        print(f"   Confidence: {item['confidence']}")

    print("\n" + "=" * 60)
    print("UNCERTAINTIES")
    print("=" * 60)

    if data["uncertainties"]:
        for uncertainty in data["uncertainties"]:
            print(f"- {uncertainty}")
    else:
        print("- None reported.")

    print("\n" + "=" * 60)
    print("QUALITY REVIEW")
    print("=" * 60)

    warnings = data.get("quality_warnings", [])

    if warnings:
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("- No structural warnings detected.")

    print("\n" + "=" * 60)
    print("FINAL NOTE")
    print("=" * 60)

    print("Detections are model-generated and unverified.")
    print("Possible interpretations are rule-based candidates.")
    print("No ISO compliance or handling safety is certified.")
    print("Human verification is required.")


def main() -> None:
    image_path = input("Enter image path: ").strip().strip('"').strip("'")

    try:
        print("\nAnalyzing shipping image...")
        result = analyze_shipping_image(image_path)
        print_report(result)

    except (
        FileNotFoundError,
        ValueError,
        json.JSONDecodeError,
    ) as error:
        print(f"\nValidation error: {error}")

    except ResponseError as error:
        print(f"\nOllama model error: {error}")

    except ConnectionError:
        print("\nConnection error: Ollama is unavailable.")

    except Exception as error:
        print(f"\nUnexpected error: " f"{type(error).__name__}: {error}")


if __name__ == "__main__":
    main()
