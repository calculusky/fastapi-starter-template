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
from datetime import datetime, timedelta

#
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
# from database.db import asyncSession



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearerScheme = HTTPBearer()


def verifyPassword(password, hashedPassword):
    return pwd_context.verify(password, hashedPassword)

def hashPassword(password):
    return pwd_context.hash(password)

def createAccessToken(data: dict, expiresDelta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expiresDelta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=config.jwtSecret)
    return encoded_jwt


def getUser(db: list[dict], email: str):
    user_dict = next(filter(lambda user: user["email"] == email, db), None)
    if user_dict:
        return schema.User(**user_dict)
    


def authenticateUser(fake_db, email: str, password: str):
    user = getUser(fake_db, email)
    print(user, email, password)
    if not user:
        return False
    if not verifyPassword(password, user.hashedPassword):
        return False
    return user





async def getLoggedInUser(credentials: HTTPAuthorizationCredentials = Depends(bearerScheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, config.jwtSecret)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schema.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = {} # getUser(fake_users_db, email=token_data.email)
    if user is None:
         raise credentials_exception
    return user

async def verifyEmail(options: schema.VerifyEmailSchema, session: AsyncSession):
    stmt = select(model.User).where(model.User.email == options.email)
    result = await session.execute(stmt)
    user = result.scalars().first()
    if user:
        raise errors.DuplicateUserException(detail="Account already exists",  status_code=status.HTTP_400_BAD_REQUEST)
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
    
        

async def login(options: schema.LoginSchema):
    user = {}  # authenticateUser(fake_users_db, options.email, options.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    tokenExpire = timedelta(minutes=config.jwtTokenExpire)
    accessToken = createAccessToken(
        data={"sub": user.email}, expiresDelta=tokenExpire
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
        raise errors.DuplicateUserException(detail="Account already exists. Kindly login",  status_code=status.HTTP_400_BAD_REQUEST)
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
        return data
    except:
        await session.rollback()
        raise errors.AccountCreationException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Failed to create user account")
    
    
    
   





