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


def load_json(file_path: str) -> list[dict[str, Any]]:
    """Carga datos desde un archivo JSON."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_json(file_path: str, data: list[dict[str, Any]]):
    """Guarda datos en un archivo JSON."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False, default=str)


# Funciones para usuarios
def get_next_usuario_id() -> int:
    """Obtiene el siguiente ID disponible para usuarios."""
    usuarios = load_json(USUARIOS_FILE)
    return max(usuario.get("id", 0) for usuario in usuarios) + 1 if usuarios else 1


def get_usuario_by_email(email: str) -> Optional[UsuarioDB]:
    """Busca un usuario por email."""
    usuarios = load_json(USUARIOS_FILE)
    return next((UsuarioDB(**u) for u in usuarios if u["email"] == email), None)


def get_usuario_by_id(user_id: int) -> Optional[UsuarioDB]:
    """Busca un usuario por ID."""
    usuarios = load_json(USUARIOS_FILE)
    return next((UsuarioDB(**u) for u in usuarios if u["id"] == user_id), None)


def save_usuario(usuario: UsuarioDB):
    """Guarda un usuario en el archivo JSON."""
    usuarios = load_json(USUARIOS_FILE)
    usuarios.append(usuario.model_dump())
    save_json(USUARIOS_FILE, usuarios)


def update_usuario(user_id: int, updates: dict[str, Any]):
    """Actualiza un usuario con los datos proporcionados."""
    try:
        usuarios = load_json(USUARIOS_FILE)
        for i, u in enumerate(usuarios):
            if u["id"] == user_id:
                usuarios[i].update(updates)
                save_json(USUARIOS_FILE, usuarios)
    except Exception as e:
        print(f"Error al actualizar usuario: {e}")
        return False
    return True


# Funciones para torneos
def get_next_torneo_id() -> int:
    """Obtiene el siguiente ID disponible para torneos."""
    torneos = load_json(TORNEOS_FILE)
    return max(t.get("id", 0) for t in torneos) + 1 if torneos else 1


def get_torneo_by_id(torneo_id: int) -> Optional[TorneoDB]:
    """Busca un torneo por ID."""
    torneos = load_json(TORNEOS_FILE)
    return next((TorneoDB(**t) for t in torneos if t["id"] == torneo_id), None)


def get_torneos_by_organizador(organizador_id: int) -> list[TorneoDB]:
    """Obtiene todos los torneos de un organizador."""
    torneos = load_json(TORNEOS_FILE)
    return [TorneoDB(**t) for t in torneos if t["organizador_id"] == organizador_id]


def save_torneo(torneo: TorneoDB):
    """Guarda un torneo en el archivo JSON."""
    torneos = load_json(TORNEOS_FILE)
    torneos.append(torneo.model_dump())
    save_json(TORNEOS_FILE, torneos)


# Funciones para inscripciones
def get_next_inscripcion_id() -> int:
    """Obtiene el siguiente ID disponible para inscripciones."""
    inscripciones = load_json(INSCRIPCIONES_FILE)
    return max(i.get("id", 0) for i in inscripciones) + 1 if inscripciones else 1


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
    inscripciones.append(inscripcion.model_dump())
    save_json(INSCRIPCIONES_FILE, inscripciones)


# Funciones para partidas
def get_next_partida_id() -> int:
    """Obtiene el siguiente ID disponible para partidas."""
    partidas = load_json(PARTIDAS_FILE)
    return max(p.get("id", 0) for p in partidas) + 1 if partidas else 1


def get_partidas_by_torneo(torneo_id: int) -> list[PartidaDB]:
    """Obtiene todas las partidas de un torneo."""
    partidas = load_json(PARTIDAS_FILE)
    return [PartidaDB(**p) for p in partidas if p["torneo_id"] == torneo_id]


def save_partida(partida: PartidaDB):
    """Guarda una partida en el archivo JSON."""
    partidas = load_json(PARTIDAS_FILE)
    partidas.append(partida.model_dump())
    save_json(PARTIDAS_FILE, partidas)


# Funciones para ratings
def get_ratings_by_usuario(user_id: int) -> list[RatingDB]:
    """Obtiene todos los ratings de un usuario."""
    ratings = load_json(RATINGS_FILE)
    return [RatingDB(**r) for r in ratings if r["usuario_id"] == user_id]


def save_rating(rating: RatingDB):
    """Guarda un rating en el archivo JSON."""
    ratings = load_json(RATINGS_FILE)
    ratings.append(rating.model_dump())
    save_json(RATINGS_FILE, ratings)
