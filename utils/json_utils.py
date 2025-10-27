import json
import os
from typing import Optional, Any
from constants import UsuarioDB, TorneoDB, InscripcionDB, PartidaDB, RatingDB

# Rutas de archivos JSON
DATA_DIR = "data"
USUARIOS_FILE = os.path.join(DATA_DIR, "usuarios.json")
TORNEOS_FILE = os.path.join(DATA_DIR, "torneos.json")
INSCRIPCIONES_FILE = os.path.join(DATA_DIR, "inscripciones.json")
PARTIDAS_FILE = os.path.join(DATA_DIR, "partidas.json")
RATINGS_FILE = os.path.join(DATA_DIR, "ratings.json")


def ensure_data_dir():
    """Asegura que el directorio data existe."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_json(file_path: str) -> list[dict[str, Any]]:
    """Carga datos desde un archivo JSON."""
    ensure_data_dir()
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_json(file_path: str, data: list[dict[str, Any]]):
    """Guarda datos en un archivo JSON."""
    ensure_data_dir()
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)


# Funciones para usuarios
def get_next_usuario_id() -> int:
    """Obtiene el siguiente ID disponible para usuarios."""
    usuarios = load_json(USUARIOS_FILE)
    if not usuarios:
        return 1
    return max(u.get("id", 0) for u in usuarios) + 1


def get_usuario_by_email(email: str) -> Optional[UsuarioDB]:
    """Busca un usuario por email."""
    usuarios = load_json(USUARIOS_FILE)
    for u in usuarios:
        if u["email"] == email:
            return UsuarioDB(**u)
    return None


def get_usuario_by_id(user_id: int) -> Optional[UsuarioDB]:
    """Busca un usuario por ID."""
    usuarios = load_json(USUARIOS_FILE)
    for u in usuarios:
        if u["id"] == user_id:
            return UsuarioDB(**u)
    return None


def save_usuario(usuario: UsuarioDB):
    """Guarda un usuario en el archivo JSON."""
    usuarios = load_json(USUARIOS_FILE)
    # Remover usuario existente si existe
    usuarios = [u for u in usuarios if u["id"] != usuario.id]
    usuarios.append(usuario.dict())
    save_json(USUARIOS_FILE, usuarios)


def update_usuario(user_id: int, updates: dict[str, Any]) -> bool:
    """Actualiza un usuario con los datos proporcionados."""
    usuarios = load_json(USUARIOS_FILE)
    for i, u in enumerate(usuarios):
        if u["id"] == user_id:
            usuarios[i].update(updates)
            save_json(USUARIOS_FILE, usuarios)
            return True
    return False


# Funciones para torneos
def get_next_torneo_id() -> int:
    """Obtiene el siguiente ID disponible para torneos."""
    torneos = load_json(TORNEOS_FILE)
    if not torneos:
        return 1
    return max(t.get("id", 0) for t in torneos) + 1


def get_torneo_by_id(torneo_id: int) -> Optional[TorneoDB]:
    """Busca un torneo por ID."""
    torneos = load_json(TORNEOS_FILE)
    for t in torneos:
        if t["id"] == torneo_id:
            return TorneoDB(**t)
    return None


def get_torneos_by_organizador(organizador_id: int) -> list[TorneoDB]:
    """Obtiene todos los torneos de un organizador."""
    torneos = load_json(TORNEOS_FILE)
    return [TorneoDB(**t) for t in torneos if t["organizador_id"] == organizador_id]


def save_torneo(torneo: TorneoDB):
    """Guarda un torneo en el archivo JSON."""
    torneos = load_json(TORNEOS_FILE)
    # Remover torneo existente si existe
    torneos = [t for t in torneos if t["id"] != torneo.id]
    torneos.append(torneo.dict())
    save_json(TORNEOS_FILE, torneos)


# Funciones para inscripciones
def get_next_inscripcion_id() -> int:
    """Obtiene el siguiente ID disponible para inscripciones."""
    inscripciones = load_json(INSCRIPCIONES_FILE)
    if not inscripciones:
        return 1
    return max(i.get("id", 0) for i in inscripciones) + 1


def get_inscripciones_by_usuario(user_id: int) -> list[InscripcionDB]:
    """Obtiene todas las inscripciones de un usuario."""
    inscripciones = load_json(INSCRIPCIONES_FILE)
    return [InscripcionDB(**i) for i in inscripciones if i["usuario_id"] == user_id]


def get_inscripciones_by_torneo(torneo_id: int) -> list[InscripcionDB]:
    """Obtiene todas las inscripciones de un torneo."""
    inscripciones = load_json(INSCRIPCIONES_FILE)
    return [InscripcionDB(**i) for i in inscripciones if i["torneo_id"] == torneo_id]


def save_inscripcion(inscripcion: InscripcionDB):
    """Guarda una inscripción en el archivo JSON."""
    inscripciones = load_json(INSCRIPCIONES_FILE)
    # Remover inscripción existente si existe
    inscripciones = [i for i in inscripciones if i["id"] != inscripcion.id]
    inscripciones.append(inscripcion.dict())
    save_json(INSCRIPCIONES_FILE, inscripciones)


# Funciones para partidas
def get_next_partida_id() -> int:
    """Obtiene el siguiente ID disponible para partidas."""
    partidas = load_json(PARTIDAS_FILE)
    if not partidas:
        return 1
    return max(p.get("id", 0) for p in partidas) + 1


def get_partidas_by_torneo(torneo_id: int) -> list[PartidaDB]:
    """Obtiene todas las partidas de un torneo."""
    partidas = load_json(PARTIDAS_FILE)
    return [PartidaDB(**p) for p in partidas if p["torneo_id"] == torneo_id]


def save_partida(partida: PartidaDB):
    """Guarda una partida en el archivo JSON."""
    partidas = load_json(PARTIDAS_FILE)
    # Remover partida existente si existe
    partidas = [p for p in partidas if p["id"] != partida.id]
    partidas.append(partida.dict())
    save_json(PARTIDAS_FILE, partidas)


# Funciones para ratings
def get_ratings_by_usuario(user_id: int) -> list[RatingDB]:
    """Obtiene todos los ratings de un usuario."""
    ratings = load_json(RATINGS_FILE)
    return [RatingDB(**r) for r in ratings if r["usuario_id"] == user_id]


def save_rating(rating: RatingDB):
    """Guarda un rating en el archivo JSON."""
    ratings = load_json(RATINGS_FILE)
    ratings.append(rating.dict())
    save_json(RATINGS_FILE, ratings)
