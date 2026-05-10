import os
import sqlite3
from typing import Any


def get_db_path() -> str:
    """Retorna o caminho do banco SQLite.

    O uso da variável DB_PATH facilita testes sem alterar o código principal.
    """
    return os.getenv("DB_PATH", "performance.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Cria a tabela principal caso ela ainda não exista."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS focus_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nivel_foco INTEGER NOT NULL CHECK(nivel_foco BETWEEN 1 AND 5),
                tempo_minutos INTEGER NOT NULL CHECK(tempo_minutos > 0),
                comentario TEXT NOT NULL,
                categoria TEXT NOT NULL DEFAULT 'geral',
                tags TEXT NOT NULL DEFAULT '',
                data_registro TEXT NOT NULL
            )
            """
        )
        conn.commit()


def insert_focus_record(record: dict[str, Any]) -> dict[str, Any]:
    """Insere um registro de foco e retorna o registro salvo."""
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO focus_records
                (nivel_foco, tempo_minutos, comentario, categoria, tags, data_registro)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                record["nivel_foco"],
                record["tempo_minutos"],
                record["comentario"],
                record["categoria"],
                record["tags"],
                record["data_registro"],
            ),
        )
        conn.commit()
        saved = conn.execute(
            "SELECT * FROM focus_records WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
        return dict(saved)


def list_focus_records() -> list[dict[str, Any]]:
    """Lista todos os registros salvos em ordem de criação."""
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM focus_records ORDER BY id ASC").fetchall()
        return [dict(row) for row in rows]
