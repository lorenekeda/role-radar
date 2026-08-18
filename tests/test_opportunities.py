from fastapi.testclient import TestClient

from app.main import app


# client = TestClient(app)


def test_get_opportunities(client: TestClient):
    response = client.get("/opportunities/")

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "page" in data
    assert "limit" in data
    assert "total" in data
    assert "pages" in data

def test_get_remote_opportunities(client: TestClient, sample_opportunities):
    response = client.get("/opportunities/?remote=true")

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) == 2

    for opportunity in data["items"]:
        assert opportunity["remote"] is True

def test_search_opportunities(
    client: TestClient,
    sample_opportunities,
):
    response = client.get("/opportunities/?search=software")

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "Remote Software Engineer"

def test_pagination(
    client: TestClient,
    sample_opportunities,
):
    response = client.get("/opportunities/?page=1&limit=2")

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) == 2
    assert data["page"] == 1
    assert data["limit"] == 2
    assert data["total"] == 3
    assert data["pages"] == 2

def test_get_opportunity_not_found(client: TestClient):
    response = client.get("/opportunities/999999")

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Opportunity not found"

def test_country_filter(
    client: TestClient,
    sample_opportunities,
):
    response = client.get("/opportunities/?country=Germany")

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) == 2

    for opportunity in data["items"]:
        assert opportunity["country"] == "Germany"

def test_city_filter(
    client: TestClient,
    sample_opportunities,
):
    response = client.get("/opportunities/?city=Berlin")

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) == 1
    assert data["items"][0]["city"] == "Berlin"

def test_combined_filters(
    client: TestClient,
    sample_opportunities,
):
    response = client.get(
        "/opportunities/?country=Germany&city=Berlin&remote=true"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) == 1

    opportunity = data["items"][0]

    assert opportunity["country"] == "Germany"
    assert opportunity["city"] == "Berlin"
    assert opportunity["remote"] is True

def test_sort_by_title_ascending(
    client: TestClient,
    sample_opportunities,
):
    response = client.get(
        "/opportunities/?sort_by=title&order=asc"
    )

    assert response.status_code == 200

    data = response.json()

    titles = [opportunity["title"] for opportunity in data["items"]]

    assert titles == sorted(titles)

def test_sort_by_title_descending(
    client: TestClient,
    sample_opportunities,
):
    response = client.get(
        "/opportunities/?sort_by=title&order=desc"
    )

    assert response.status_code == 200

    data = response.json()

    titles = [opportunity["title"] for opportunity in data["items"]]

    assert titles == sorted(titles, reverse=True)


def test_invalid_sort_field(
    client: TestClient,
    sample_opportunities,
):
    response = client.get(
        "/opportunities/?sort_by=invalid_field"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid sort field: invalid_field"


def test_invalid_sort_order(
    client: TestClient,
    sample_opportunities,
):
    response = client.get(
        "/opportunities/?order=random"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Order must be 'asc' or 'desc'"


def test_create_opportunity(client: TestClient):
    opportunity = {
        "title": "Test Software Engineer",
        "company": "Test Corp",
        "location": "Toronto",
        "city": "Toronto",
        "country": "Canada",
        "url": "https://example.com/test-software-engineer",
        "salary_min": 70000,
        "salary_max": 90000,
        "salary_currency": "CAD",
        "date_posted": "2026-08-12",
        "deadline": None,
        "description": "Test opportunity",
        "source": "Test",
        "remote": True,
    }

    response = client.post(
        "/opportunities/",
        json=opportunity,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Test Software Engineer"
    assert data["company"] == "Test Corp"
    assert data["remote"] is True

def test_update_opportunity(
    client: TestClient,
    sample_opportunities,
):
    opportunity_id = sample_opportunities[0].id

    response = client.put(
        f"/opportunities/{opportunity_id}",
        json={
            "title": "Updated Software Engineer",
            "remote": False,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Updated Software Engineer"
    assert data["remote"] is False

def test_delete_opportunity(
    client: TestClient,
    sample_opportunities,
):
    opportunity_id = sample_opportunities[0].id

    response = client.delete(
        f"/opportunities/{opportunity_id}"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Opportunity deleted successfully"

    response = client.get(
        f"/opportunities/{opportunity_id}"
    )

    assert response.status_code == 404

def test_mock_ingestion(client: TestClient):
    response = client.post("/ingestion/mock")

    assert response.status_code == 200

    data = response.json()

    assert data["source"] == "MockOpportunitySource"
    assert data["found"] > 0
    assert data["created"] == data["found"]
    assert data["updated"] == 0

def test_mock_ingestion_deduplicates(client: TestClient):
    first_response = client.post("/ingestion/mock")

    assert first_response.status_code == 200

    first_data = first_response.json()

    second_response = client.post("/ingestion/mock")

    assert second_response.status_code == 200

    second_data = second_response.json()

    assert first_data["created"] == first_data["found"]
    assert second_data["created"] == 0
    assert second_data["found"] == first_data["found"]