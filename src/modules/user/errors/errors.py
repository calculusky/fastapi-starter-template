from fastapi import HTTPException

class DuplicateUserException(HTTPException):
    pass
class UserNotFoundException(HTTPException):
    pass