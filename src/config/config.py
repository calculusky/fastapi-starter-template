import os
from dotenv import load_dotenv
load_dotenv()


#TODO: validate env

jwtSecret = os.environ.get("JWT_SECRET")
jwtTokenExpire = int(os.environ.get("JWT_TOKEN_EXPIRE"))
databaseUrl = os.environ.get("DATABASE_URL")

isDevEnvironment = bool(os.getenv("DEV_ENVIRONMENT"))

print(isDevEnvironment)