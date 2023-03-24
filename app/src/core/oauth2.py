from datetime import timedelta, datetime
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import config
from jose import jwt
from src.schemas.auth_schema import Token


class JwtHandler:
    @classmethod
    def create_access_token(cls, uid: str,  exp_time: int = 0) -> str:
        """
        This function allows you to create a jwt token based on data
        uid: user_id
        data: data dictionary
        """

        now = datetime.utcnow()

        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(minutes=exp_time),
            'sub': uid,
            'type': 'access'
        }
        token = jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITHM)
        return token

    @classmethod
    def decode_access_token(cls, token: str):
        """
        This function decrypts a jwt token
        token: jwt
        """
        try:
            encoded_jwt = jwt.decode(token, config.SECRET_KEY, config.ALGORITHM)
        except jwt.JWTError:
            return None
        return encoded_jwt


async def create_tokens(user_id: str) -> Token:
    authorize = JwtHandler()
    access_token = authorize.create_access_token(user_id, exp_time=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    data = {'access_token': access_token,
            'access_time': config.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            'refresh_token': ''}

    return Token(**data)


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            token = JwtHandler().decode_access_token(credentials.credentials)
            if token is None:
                return
            return credentials.credentials
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid auth token')
