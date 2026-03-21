from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.app.application.entities.viewer import AuthenticatedUser
from src.app.container import Container
from src.app.infra.jwt.jwt_service import JwtService

security = HTTPBearer(auto_error=True)


@inject
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    jwt_service: JwtService = Depends(Provide[Container.jwt_service]),
) -> AuthenticatedUser:
    return jwt_service.decode_access_token(credentials.credentials)
