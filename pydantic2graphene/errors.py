class Pydantic2GrapheneException(Exception):

    pass


class FieldNotSupported(Pydantic2GrapheneException):
    pass


class InvalidType(Pydantic2GrapheneException):
    pass


class InvalidListType(FieldNotSupported):
    pass


class InvalidConfigClass(Pydantic2GrapheneException):
    pass
