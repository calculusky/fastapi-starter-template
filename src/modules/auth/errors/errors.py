from fastapi import Depends, HTTPException, status


class DuplicateUserException(HTTPException):
    pass

class AccountVerificationException(HTTPException):
    pass

class OTPExpirationException(HTTPException):
    pass

class AccountCreationException(HTTPException):
    pass