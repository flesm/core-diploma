from uuid import UUID

from jose import JWTError, jwt

from src.app.application.entities.viewer import AuthenticatedUser
from src.app.application.exceptions import UnauthorizedException
from src.app.config import Config


class JwtService:
    def __init__(self, config: Config) -> None:
        self._secret = config.JWT.access_secret_key
        self._algorithm = config.JWT.algorithm

    def decode_access_token(self, token: str) -> AuthenticatedUser:
        try:
            payload = jwt.decode(
                token, self._secret, algorithms=[self._algorithm]
            )
        except JWTError as exc:
            raise UnauthorizedException("Invalid or expired access token.") from exc

        role = payload.get("role")
        if not payload.get("user_id") or not payload.get("email") or not role:
            raise UnauthorizedException("Access token payload is invalid.")

        return AuthenticatedUser(
            user_id=UUID(payload["user_id"]),
            email=payload["email"],
            role=role,
            is_staff=bool(payload.get("is_staff", False)),
        )
