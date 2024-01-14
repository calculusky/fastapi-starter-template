from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from modules.auth.schema import schema
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from core.utils import utils
from config import config, constant
import shortuuid
from sqlalchemy import select
from database import model
from ..errors import errors
from modules.user.errors.errors import UserNotFoundException, DuplicateUserException 
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import getDb





pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearerScheme = HTTPBearer()


def verifyPassword(password, hashedPassword):
    return pwd_context.verify(password, hashedPassword)

def hashPassword(password):
    return pwd_context.hash(password)

def createAccessToken(data: dict):
    to_encode = data.copy()
    tokenExpire = datetime.utcnow() + timedelta(minutes=config.jwtTokenExpire)
    to_encode.update({"exp": tokenExpire})
    encoded_jwt = jwt.encode(to_encode, key=config.jwtSecret)
    return encoded_jwt


async def authGuard(authCred: HTTPAuthorizationCredentials = Depends(bearerScheme), session: AsyncSession = Depends(getDb)):
    try:
        payload = jwt.decode(authCred.credentials, config.jwtSecret)
        identifier: str = payload.get("sub")
        if identifier is None:
            raise errors.GenericAuthException(
                 status_code=status.HTTP_401_UNAUTHORIZED,
                 detail="Your session is unauthorized",
            )
        tokenData = schema.TokenData(identifier=identifier)
        stmt = select(model.User).where(model.User.identifier == tokenData.identifier)
        result = await session.execute(stmt)
        user = result.scalars().first()
        if not user:
            raise UserNotFoundException(
                 status_code=status.HTTP_401_UNAUTHORIZED,
                 detail="Your session is unauthorized",
            )
        return user
        
    except JWTError:
        raise errors.InvalidAuthTokenException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your session is unauthorized",
        )
        
 

async def verifyEmail(options: schema.VerifyEmailSchema, session: AsyncSession):
    stmt = select(model.User).where(model.User.email == options.email)
    result = await session.execute(stmt)
    user = result.scalars().first()
    if user:
        raise DuplicateUserException(detail="Account already exists",  status_code=status.HTTP_400_BAD_REQUEST)
    #TODO: send emails here
    
    email = options.email.lower()
    code = utils.generateRandomNum()
    stmt = select(model.AccountVerificationRequest).where(model.AccountVerificationRequest.email == email)
    
    result = await session.execute(stmt)
    existingData = result.scalars().first()
    
    if existingData:
        existingData.code = code
        await session.commit()
        return utils.buildResponse(message="Email verification successfully sent")
        
    body = schema.AccountVerificationRequestSchema(email=email, code=code)
    data = model.AccountVerificationRequest(**body.model_dump())
    session.add(data)
    await session.commit()
    return utils.buildResponse(message="Email verification successfully sent")
    
        

async def login(options: schema.LoginSchema, session: AsyncSession):
    stmt = select(model.User).where(model.User.email == options.email)
    result = await session.execute(stmt)
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
   
    tokenEncodeData = {"sub": user.identifier }
    accessToken = createAccessToken(
        data=tokenEncodeData
    )

    return utils.buildResponse(
        message="login successful", 
        data={
        "accessToken": accessToken,
        "tokenType": "bearer"    
    })

async def signup(options: schema.SignupSchema, session: AsyncSession):
    email = options.email.lower()
    stmt = select(model.User).where(model.User.email == options.email)
    result = await session.execute(stmt)
    user = result.scalars().first()
    if user:
        raise DuplicateUserException(detail="Account already exists. Kindly login", status_code=status.HTTP_400_BAD_REQUEST)
    getCodeStmt = select(model.AccountVerificationRequest).where(model.AccountVerificationRequest.code == options.code, model.AccountVerificationRequest.email == email)
    result = await session.execute(getCodeStmt)
    verifyDataObj = result.scalars().first()
    if not verifyDataObj:
        raise errors.AccountVerificationException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid verification code")
    
    timeDifference = datetime.utcnow().timestamp() - verifyDataObj.updatedAt.timestamp()
    if timeDifference > constant.OTP_EXPIRATION_TIME:
        raise errors.OTPExpirationException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your verification code has expired. Kindly request for a new one")
    
    identifier = shortuuid.ShortUUID().random(length=15)
    schemaData = schema.CreateUser(
        firstName=options.firstName,
        email=options.email,
        lastName=options.lastName,
        identifier=identifier,
        password=hashPassword(options.password)
    )
           
    data = model.User(**schemaData.model_dump())
    
    try:
        session.add(data)
        await session.delete(verifyDataObj)
        await session.commit()
        await session.refresh(data)
        tokenEncodeData = {"sub": data.identifier }
        accessToken = createAccessToken(
            data=tokenEncodeData
        )
        
        return utils.buildResponse(
            message="signup successful", 
            data={
            "accessToken": accessToken,
            "tokenType": "bearer"    
        })
    except:
        await session.rollback()
        raise errors.AccountCreationException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Failed to create user account")
    
    
    
   





