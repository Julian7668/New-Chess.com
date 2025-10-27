from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from constants.modelos import (
    UsuarioCrear,
    UsuarioRespuesta,
    LoginRequest,
    Token,
    UsuarioActualizar,
    CambiarPassword,
)
from auth.hash_password import hash_password, verify_password
from auth.jwt_handler import (
    create_access_token,
    create_refresh_token,
    refresh_access_token,
)
from auth.dependencies import get_current_user
from utils.json_utils import (
    get_usuario_by_email,
    get_next_usuario_id,
    save_usuario,
    update_usuario,
)

router = APIRouter(prefix="/auth", tags=["autenticación"])


@router.post(
    "/register", response_model=UsuarioRespuesta, status_code=status.HTTP_201_CREATED
)
async def register(usuario_data: UsuarioCrear):
    """
    Registra un nuevo usuario en el sistema.

    - **email**: Email único del usuario
    - **password**: Contraseña (mínimo 8 caracteres)
    - **nombre**: Nombre del usuario
    - **apellido**: Apellido del usuario
    - **rol**: Rol del usuario (por defecto 'jugador')
    """
    # Verificar si el email ya existe
    if get_usuario_by_email(usuario_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado",
        )

    # Crear nuevo usuario
    user_id = get_next_usuario_id()
    hashed_password = hash_password(usuario_data.password)

    from constants.modelos import UsuarioDB

    nuevo_usuario = UsuarioDB(
        id=user_id,
        email=usuario_data.email,
        nombre=usuario_data.nombre,
        apellido=usuario_data.apellido,
        rol=usuario_data.rol,
        password_hash=hashed_password,
        fecha_creacion=datetime.utcnow(),
        activo=True,
    )

    # Guardar usuario
    save_usuario(nuevo_usuario)

    # Retornar respuesta sin contraseña
    return UsuarioRespuesta(
        id=nuevo_usuario.id,
        email=nuevo_usuario.email,
        nombre=nuevo_usuario.nombre,
        apellido=nuevo_usuario.apellido,
        rol=nuevo_usuario.rol,
        fecha_creacion=nuevo_usuario.fecha_creacion,
        activo=nuevo_usuario.activo,
    )


@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    """
    Inicia sesión y retorna tokens de acceso y refresh.

    - **email**: Email del usuario
    - **password**: Contraseña del usuario
    """
    # Buscar usuario por email
    usuario = get_usuario_by_email(login_data.email)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
        )

    # Verificar contraseña
    if not verify_password(login_data.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
        )

    # Verificar si usuario está activo
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario inactivo"
        )

    # Crear tokens
    token_data = {"user_id": usuario.id, "email": usuario.email, "rol": usuario.rol}

    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=Token)
async def refresh_token_endpoint(refresh_token: str):
    """
    Refresca el token de acceso usando un refresh token válido.

    - **refresh_token**: Token de refresh
    """
    access_token = refresh_access_token(refresh_token)
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido o expirado",
        )

    # Necesitamos obtener el refresh token original para crear uno nuevo
    # En una implementación real, guardaríamos los refresh tokens en una base de datos
    # Por simplicidad, creamos un nuevo par de tokens
    # Esto no es ideal en producción, pero funciona para el ejemplo

    # Para este ejemplo, devolveremos solo el nuevo access token
    # En producción, deberías invalidar el refresh token usado y crear uno nuevo
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.get("/me", response_model=UsuarioRespuesta)
async def get_current_user_info(
    current_user: UsuarioRespuesta = Depends(get_current_user),
):
    """
    Obtiene la información del usuario actualmente autenticado.
    """
    return current_user


@router.put("/me", response_model=UsuarioRespuesta)
async def update_profile(
    user_updates: UsuarioActualizar,
    current_user: UsuarioRespuesta = Depends(get_current_user),
):
    """
    Actualiza el perfil del usuario actualmente autenticado.

    - **nombre**: Nuevo nombre (opcional)
    - **apellido**: Nuevo apellido (opcional)
    - **email**: Nuevo email (opcional)
    """
    updates = {}
    if user_updates.nombre is not None:
        updates["nombre"] = user_updates.nombre
    if user_updates.apellido is not None:
        updates["apellido"] = user_updates.apellido
    if user_updates.email is not None:
        # Verificar que el email no esté en uso por otro usuario
        existing_user = get_usuario_by_email(user_updates.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está en uso",
            )
        updates["email"] = user_updates.email

    if updates:
        updates["fecha_actualizacion"] = datetime.utcnow()
        success = update_usuario(current_user.id, updates)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )

    # Retornar usuario actualizado
    updated_user = (
        get_usuario_by_email(current_user.email)
        if not user_updates.email
        else get_usuario_by_email(user_updates.email)
    )
    if updated_user:
        return UsuarioRespuesta(
            id=updated_user.id,
            email=updated_user.email,
            nombre=updated_user.nombre,
            apellido=updated_user.apellido,
            rol=updated_user.rol,
            fecha_creacion=updated_user.fecha_creacion,
            fecha_actualizacion=updated_user.fecha_actualizacion,
            activo=updated_user.activo,
        )

    return current_user


@router.post("/logout")
async def logout():
    """
    Cierra la sesión del usuario.

    En una implementación real, aquí invalidaríamos el refresh token
    guardándolo en una lista negra en la base de datos.
    """
    # Por simplicidad, solo retornamos un mensaje de éxito
    # En producción, deberías invalidar los tokens
    return {"message": "Sesión cerrada exitosamente"}


@router.put("/change-password")
async def change_password(
    password_data: CambiarPassword,
    current_user: UsuarioRespuesta = Depends(get_current_user),
):
    """
    Cambia la contraseña del usuario actualmente autenticado.

    - **password_actual**: Contraseña actual
    - **password_nueva**: Nueva contraseña (mínimo 8 caracteres)
    """
    from utils.json_utils import get_usuario_by_id as get_full_user

    # Obtener usuario completo con hash de contraseña
    full_user = get_full_user(current_user.id)
    if not full_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    # Verificar contraseña actual
    if not verify_password(password_data.password_actual, full_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña actual incorrecta",
        )

    # Hash de nueva contraseña
    new_hashed_password = hash_password(password_data.password_nueva)

    # Actualizar contraseña
    updates = {
        "password_hash": new_hashed_password,
        "fecha_actualizacion": datetime.utcnow(),
    }

    success = update_usuario(current_user.id, updates)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar contraseña",
        )

    return {"message": "Contraseña cambiada exitosamente"}
