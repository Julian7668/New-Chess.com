import os
from typing import cast

# Configuración JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")

if None in (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
):
    raise ValueError(
        "SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES o REFRESH_TOKEN_EXPIRE_DAYS no están configuradas."
    )
ACCESS_TOKEN_EXPIRE_MINUTES = int(cast(str, ACCESS_TOKEN_EXPIRE_MINUTES))
REFRESH_TOKEN_EXPIRE_DAYS = int(cast(str, REFRESH_TOKEN_EXPIRE_DAYS))

# Roles de usuario
ROLES = {
    "jugador": "jugador",
    "organizador": "organizador",
    "arbitro": "arbitro",
    "admin": "admin",
}

# Estados de torneo
ESTADOS_TORNEO = {
    "abierto": "abierto",
    "en_curso": "en_curso",
    "finalizado": "finalizado",
}

# Formatos de torneo
FORMATOS_TORNEO = {
    "suizo": "suizo",
    "round_robin": "round_robin",
    "eliminacion": "eliminacion",
}

# Resultados de partida
RESULTADOS_PARTIDA = {
    "blancas_ganan": "blancas_ganan",
    "negras_ganan": "negras_ganan",
    "tablas": "tablas",
    "no_jugada": "no_jugada",
}
