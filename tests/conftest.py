import os

os.environ["TEST"] = "true"

import pytest  # noqa: E402

from resultsdb_frontend import app  # noqa: E402


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
