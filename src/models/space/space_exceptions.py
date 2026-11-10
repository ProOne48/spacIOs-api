class SpaceGeneralError(Exception):
    """General error for space model"""

    message: str
    error_code: str

    def __init__(
        self, msg: str = "Space error", error_code: str = "Space.General-error"
    ):
        self.message = msg
        self.error_code = error_code

        super().__init__(msg, error_code)


class SpaceNoPDFError(SpaceGeneralError):
    """Error for when a space has no PDF"""

    def __init__(self, msg: str = "Space has no PDF", error_code: str = "Space.No-PDF"):
        super().__init__(msg, error_code)


class SpaceNoOwnerError(SpaceGeneralError):
    """Error for when a space has no owner"""

    def __init__(
        self, msg: str = "Space has no owner", error_code: str = "Space.No-Owner"
    ):
        super().__init__(msg, error_code)


class SpaceTableNotFoundError(SpaceGeneralError):
    """Error for when a table is not found in a space"""

    def __init__(
        self,
        msg: str = "Table not found in space",
        error_code: str = "Space.Table-Not-Found",
    ):
        super().__init__(msg, error_code)
