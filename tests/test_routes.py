from unittest.mock import patch

MOCK_RESULTS = {
    "data": [
        {
            "id": 1,
            "testcase": {"name": "test.case.1"},
            "outcome": "PASSED",
            "groups": ["group1"],
            "data": {},
            "note": "",
            "submit_time": "2024-01-01T00:00:00",
            "href": "",
            "ref_url": "",
        }
    ],
    "prev": None,
    "next": None,
}

MOCK_RESULT = {
    "id": 1,
    "testcase": {"name": "test.case.1", "url": ""},
    "outcome": "PASSED",
    "groups": ["group1"],
    "note": "",
    "submit_time": "2024-01-01T00:00:00",
    "data": {},
    "href": "",
    "ref_url": "",
}

MOCK_GROUPS = {
    "data": [{"uuid": "group1", "results_count": 1}],
    "prev": None,
    "next": None,
}

MOCK_GROUP = {"uuid": "group1", "results_count": 1}

MOCK_TESTCASES = {
    "data": [{"name": "test.case.1"}],
    "prev": None,
    "next": None,
}

MOCK_TESTCASE = {"name": "test.case.1"}


def test_index_redirects(client):
    response = client.get("/")
    assert response.status_code == 302
    assert "/results" in response.headers["Location"]


@patch("resultsdb_frontend.controllers.main.RDB_API")
def test_results(mock_api, client):
    mock_api.get_results.return_value = MOCK_RESULTS
    response = client.get("/results")
    assert response.status_code == 200


@patch("resultsdb_frontend.controllers.main.RDB_API")
def test_result_detail(mock_api, client):
    mock_api.get_result.return_value = MOCK_RESULT
    response = client.get("/results/1")
    assert response.status_code == 200


@patch("resultsdb_frontend.controllers.main.RDB_API")
def test_result_detail_no_groups(mock_api, client):
    mock_api.get_result.return_value = {
        "id": 1,
        "testcase": {"name": "test.case.1", "url": ""},
        "outcome": "PASSED",
        "note": "",
        "submit_time": "2024-01-01T00:00:00",
        "data": {},
        "href": "",
        "ref_url": "",
    }
    response = client.get("/results/1")
    assert response.status_code == 200


@patch("resultsdb_frontend.controllers.main.RDB_API")
def test_groups(mock_api, client):
    mock_api.get_groups.return_value = MOCK_GROUPS
    response = client.get("/groups")
    assert response.status_code == 200


@patch("resultsdb_frontend.controllers.main.RDB_API")
def test_group_detail(mock_api, client):
    mock_api.get_group.return_value = MOCK_GROUP
    response = client.get("/groups/group1")
    assert response.status_code == 200


@patch("resultsdb_frontend.controllers.main.RDB_API")
def test_testcases(mock_api, client):
    mock_api.get_testcases.return_value = MOCK_TESTCASES
    response = client.get("/testcases")
    assert response.status_code == 200


@patch("resultsdb_frontend.controllers.main.RDB_API")
def test_testcase_detail(mock_api, client):
    mock_api.get_testcase.return_value = MOCK_TESTCASE
    response = client.get("/testcases/test.case.1")
    assert response.status_code == 200


@patch("resultsdb_frontend.controllers.main.RDB_API")
def test_testcase_tokenizer(mock_api, client):
    mock_api.get_testcases.side_effect = [
        {"data": [{"name": "b.test"}, {"name": "a.test"}]},
        {"data": []},
    ]
    response = client.get("/testcase_tokenizer")
    assert response.status_code == 200
    assert response.content_type == "application/json"
    data = response.get_json()
    assert data == ["a.test", "b.test"]
