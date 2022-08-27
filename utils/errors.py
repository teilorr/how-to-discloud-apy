class RequestError(Exception):
    def __init__(self, msg: str, **params) -> None:
        msg = msg.format(**params) if params else msg
        super().__init__(msg)
