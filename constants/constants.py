import os

# Configuración JWT
SECRET_KEY = os.getenv(
    "SECRET_KEY", "tu_clave_secreta_muy_segura_aqui"
)  # En producción, usar variable de entorno
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

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
