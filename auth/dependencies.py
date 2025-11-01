from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth import verify_token
from utils import get_usuario_by_id
from constants import TokenData, UsuarioRespuesta, ROLES

# Esquema de seguridad para Bearer tokens
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UsuarioRespuesta:
    """
    Dependencia para obtener el usuario actual desde el token JWT.

    Args:
        credentials: Credenciales del header Authorization

    Returns:
        UsuarioRespuesta: Datos del usuario autenticado

    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    token = credentials.credentials
    token_data = verify_token(token, "access")

    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuario = get_usuario_by_id(token_data.user_id)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Convertir UsuarioDB a UsuarioRespuesta
    return UsuarioRespuesta(
        id=usuario.id,
        email=usuario.email,
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        rol=usuario.rol,
        fecha_creacion=usuario.fecha_creacion,
        fecha_actualizacion=usuario.fecha_actualizacion,
        activo=usuario.activo,
    )


def get_current_token_data(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> TokenData:
    """
    Dependencia para obtener los datos del token sin cargar el usuario completo.

    Args:
        credentials: Credenciales del header Authorization

    Returns:
        TokenData: Datos del token decodificado

    Raises:
        HTTPException: Si el token es inválido
    """
    token = credentials.credentials
    token_data = verify_token(token, "access")

    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token_data


def require_role(required_roles: list):
    """
    Crea una dependencia que requiere uno o más roles específicos.

    Args:
        required_roles: Lista de roles permitidos

    Returns:
        Función de dependencia que verifica el rol del usuario
    """

    def role_checker(current_user: UsuarioRespuesta = Depends(get_current_user)):
        if current_user.rol not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere uno de los siguientes roles: {', '.join(required_roles)}",
            )
        return current_user

    return role_checker


# Dependencias específicas para roles comunes
require_jugador = require_role([ROLES["jugador"]])
require_organizador = require_role([ROLES["organizador"]])
require_arbitro = require_role([ROLES["arbitro"]])
require_admin = require_role([ROLES["admin"]])

# Dependencias para múltiples roles
require_organizador_or_admin = require_role([ROLES["organizador"], ROLES["admin"]])
require_arbitro_or_admin = require_role([ROLES["arbitro"], ROLES["admin"]])
require_organizador_or_arbitro_or_admin = require_role(
    [ROLES["organizador"], ROLES["arbitro"], ROLES["admin"]]
)
