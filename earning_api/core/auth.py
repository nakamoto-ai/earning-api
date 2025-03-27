from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from earning_api.core.config import settings

security = HTTPBearer()


def verify_token(
        credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify Bearer token validity."""
    token = credentials.credentials
    if token != settings.TOKEN:
        raise HTTPException(status_code=401,
                            detail="Invalid or missing authentication token")
    return token
