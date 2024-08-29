from typing import Annotated, Union
from fastapi import HTTPException, Header, status
from fastapi import HTTPException
import jwt
from src.settings import SECRET_KEY


def verify_token(token: str) -> Union[str, None]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("id")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
def token_middleware(Authorization: Annotated[str, Header()]):
    return verify_token(token=Authorization.split(' ')[1])