import re


GERMAN_CITIES = {
    "Augsburg",
    "Berlin",
    "Bielefeld",
    "Cologne",
    "Dusseldorf",
    "Düsseldorf",
    "Essen",
    "Frankfurt am Main",
    "Hamburg",
    "Leipzig",
    "Mainz",
    "Munich",
    "München",
    "Münster",
    "Osnabrück",
    "Stuttgart",
}


UK_CITIES = {
    "Bristol",
    "Glasgow",
    "London",
}


def normalize_location(
    location: str | None,
) -> tuple[str | None, str | None]:

    if not location:
        return None, None

    location = location.strip()

    # Explicit country names
    if location in {"Deutschland", "Germany"}:
        return None, "Germany"

    if location == "United Kingdom":
        return None, "United Kingdom"

    # Remote-only locations
    if location.lower() == "remote":
        return None, None

    # Remove common labels
    cleaned = re.sub(
        r"\s*\((?:Hybrid|Remote)\)\s*$",
        "",
        location,
        flags=re.IGNORECASE,
    )

    cleaned = re.sub(
        r"\s+Office\s*$",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    cleaned = cleaned.strip()

    # Explicit city + country
    if "," in cleaned:
        parts = [part.strip() for part in cleaned.split(",")]

        city = parts[0]

        country = None

        if any(
            part.lower() in {"germany", "deutschland"}
            for part in parts[1:]
        ):
            country = "Germany"

        elif any(
            part.lower() in {"uk", "united kingdom"}
            for part in parts[1:]
        ):
            country = "United Kingdom"

        if country:
            return city, country

        return city, None

    # Known German cities
    if cleaned in GERMAN_CITIES:
        return cleaned, "Germany"

    # Known UK cities
    if cleaned in UK_CITIES:
        return cleaned, "United Kingdom"

    # Explicit UK prefixes
    if cleaned.startswith("UK - "):
        return cleaned.removeprefix("UK - ").strip(), "United Kingdom"

    if cleaned.startswith("UK "):
        return cleaned.removeprefix("UK ").strip(), "United Kingdom"

    return cleaned, None