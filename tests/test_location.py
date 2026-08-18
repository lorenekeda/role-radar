from app.ingestion.location import normalize_location


def test_normalize_german_city():
    city, country = normalize_location("Berlin")

    assert city == "Berlin"
    assert country == "Germany"


def test_normalize_german_city_with_hybrid():
    city, country = normalize_location("Berlin (Hybrid)")

    assert city == "Berlin"
    assert country == "Germany"


def test_normalize_german_city_with_office():
    city, country = normalize_location("Munich Office")

    assert city == "Munich"
    assert country == "Germany"


def test_normalize_german_city_with_german_name():
    city, country = normalize_location("München")

    assert city == "München"
    assert country == "Germany"


def test_normalize_uk_city():
    city, country = normalize_location("London")

    assert city == "London"
    assert country == "United Kingdom"


def test_normalize_uk_prefix():
    city, country = normalize_location("UK London")

    assert city == "London"
    assert country == "United Kingdom"


def test_normalize_city_with_country():
    city, country = normalize_location("London, UK")

    assert city == "London"
    assert country == "United Kingdom"


def test_normalize_germany_location():
    city, country = normalize_location("Germany")

    assert city is None
    assert country == "Germany"


def test_normalize_remote():
    city, country = normalize_location("Remote")

    assert city is None
    assert country is None


def test_normalize_empty_location():
    city, country = normalize_location(None)

    assert city is None
    assert country is None