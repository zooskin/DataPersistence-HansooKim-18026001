class JsonStoreError(Exception):
    pass


class RecordNotFoundError(JsonStoreError):
    def __init__(self, id: str) -> None:
        super().__init__(f"Record not found: id='{id}'")


class DuplicateKeyError(JsonStoreError):
    def __init__(self, id: str) -> None:
        super().__init__(f"Record already exists: id='{id}'")
