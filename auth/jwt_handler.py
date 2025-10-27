from datetime import datetime, timedelta, timezone
from typing import Optional, cast
from jose import JWTError, jwt
from constants import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    TokenData,
)


def create_refresh_token(data: dict):
    """
    Crea un token de refresh JWT.

    Args:
        data: Datos a incluir en el payload del token

    Returns:
        Token JWT como string
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode |= {"exp": expire, "type": "refresh"}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Crea un token de acceso JWT.

    Args:
        data: Datos a incluir en el payload del token
        expires_delta: Tiempo de expiración opcional

    Returns:
        Token JWT como string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode |= {"exp": expire, "type": "access"}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str, token_type: str = "access") -> Optional[TokenData]:
    """
    Verifica y decodifica un token JWT.

    Args:
        token: El token JWT a verificar
        token_type: Tipo de token esperado ("access" o "refresh")

    Returns:
        TokenData si el token es válido, None en caso contrario
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_type_payload = payload.get("type")

        if token_type_payload != token_type:
            return None

        user_id = cast(int, payload.get("user_id"))
        email = cast(str, payload.get("email"))
        rol = cast(str, payload.get("rol"))

        if user_id is None or email is None or rol is None:
            return None

        return TokenData(user_id=user_id, email=email, rol=rol)
    except JWTError:
        return None


def refresh_access_token(refresh_token: str) -> Optional[str]:
    """
    Crea un nuevo token de acceso usando un refresh token.

    Args:
        refresh_token: El token de refresh

    Returns:
        Nuevo token de acceso si el refresh token es válido, None en caso contrario
    """
    token_data = verify_token(refresh_token, "refresh")
    if token_data is None:
        return None

    # Crear nuevo access token con los mismos datos
    access_token_data = {
        "user_id": token_data.user_id,
        "email": token_data.email,
        "rol": token_data.rol,
    }
    return create_access_token(access_token_data)
