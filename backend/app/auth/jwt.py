import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from backend.app.config.settings import settings
from backend.app.auth.exceptions import InvalidToken, ExpiredToken

class JWTHandler:
    """
    Handles the generation and validation of JSON Web Tokens.
    """
    def __init__(self):
        self.secret = settings.auth.jwt_secret
        self.algorithm = settings.auth.jwt_algorithm
        self.access_expire = settings.auth.access_token_expire_minutes
        self.refresh_expire = settings.auth.refresh_token_expire_days

    def create_access_token(self, data: Dict[str, Any]) -> str:
        """
        Generates a short-lived access token.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_expire)
        to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
        return jwt.encode(to_encode, self.secret, algorithm=self.algorithm)

    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """
        Generates a long-lived refresh token.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=self.refresh_expire)
        to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
        return jwt.encode(to_encode, self.secret, algorithm=self.algorithm)

    def decode_token(self, token: str) -> Dict[str, Any]:
        """
        Decodes and validates a JWT.
        Raises InvalidToken or ExpiredToken on failure.
        """
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise ExpiredToken()
        except jwt.JWTError:
            raise InvalidToken()

# Singleton instance
jwt_handler = JWTHandler()
