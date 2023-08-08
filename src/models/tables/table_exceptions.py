
class TableNumberExistError(Exception):
    def __init__(self, msg: str, error_code: str):
        super().__init__(msg, error_code)