class Route:
    base_url = "https://api.discloud.app/v2"
    def __init__(self, method: str, endpoints: str, **params) -> None:
        url = self.base_url + endpoints
        if params:
            url = url.format(**params)

        self.url = url
        self.method = method