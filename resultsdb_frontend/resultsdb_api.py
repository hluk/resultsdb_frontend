from resultsdb_frontend.requests_session import get_requests_session


def _prepare_params(**kwargs):
    return {
        key: ",".join(str(v) for v in value) if isinstance(value, list) else str(value)
        for key, value in kwargs.items()
        if value is not None
    }


class ResultsDBapi:
    def __init__(self, api_url):
        self.url = api_url.rstrip("/")
        self.session = get_requests_session()

    def _get(self, api, **kwargs):
        r = self.session.get(f"{self.url}{api}", **kwargs)
        r.raise_for_status()
        return r.json()

    def get_group(self, uuid):
        return self._get(f"/groups/{uuid}")

    def get_groups(self, **kwargs):
        return self._get("/groups", params=_prepare_params(**kwargs))

    def get_result(self, id):
        return self._get(f"/results/{id}")

    def get_results(self, **kwargs):
        return self._get("/results", params=_prepare_params(**kwargs))

    def get_testcase(self, name):
        return self._get(f"/testcases/{name}")

    def get_testcases(self, **kwargs):
        return self._get("/testcases", params=_prepare_params(**kwargs))
