from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.config import SECRET_KEY
import jwt
from jwt.exceptions import PyJWTError

security = HTTPBearer()


async def access_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            key=SECRET_KEY,
            options={
                "verify_signature": False,
                "verify_aud": False,
                "verify_iss": False,
            },
        )
        print("payload => ", payload)
        return payload
    except PyJWTError as e:
        raise HTTPException(status_code=401, detail=str(e))
