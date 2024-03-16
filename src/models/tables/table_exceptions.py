class TableNumberExistError(Exception):
    def __init__(
        self,
        msg: str = "Table number already exists",
        error_code: str = "TABLE_NUMBER_EXISTS",
    ):
        super().__init__(msg, error_code)


class TableNotExist(Exception):
    def __init__(
        self, msg: str = "Table not exists", error_code: str = "TABLE_NOT_EXISTS"
    ):
        super().__init__(msg, error_code)


class TableError(Exception):
    def __init__(self, msg: str = "Table error", error_code: str = "TABLE_ERROR"):
        super().__init__(msg, error_code)


class TableAlreadyOccupiedError(Exception):
    def __init__(
        self,
        msg: str = "Table already occupied",
        error_code: str = "TABLE_ALREADY_OCCUPIED",
    ):
        super().__init__(msg, error_code)
