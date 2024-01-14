from fastapi import HTTPException

class AccountVerificationException(HTTPException):
    pass

class OTPExpirationException(HTTPException):
    pass

class AccountCreationException(HTTPException):
    pass

class GenericAuthException(HTTPException):
    pass

class InvalidAuthTokenException(HTTPException):
    pass
