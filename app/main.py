from contextlib import asynccontextmanager

from fastapi import FastAPI, status

from app.database import init_db, insert_focus_record
from app.schemas import (
    DiagnosticoProdutividadeResponse,
    RegistroFocoCreate,
    RegistroFocoResponse,
)
from app.services import formatar_registro, gerar_diagnostico, preparar_registro


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="API de Foco e Produtividade",
    version="1.0.0",
    description=(
        "Backend para registrar blocos de trabalho e gerar um diagnóstico "
        "inteligente de produtividade."
    ),
    lifespan=lifespan,
)


@app.get("/")
def health_check() -> dict[str, str]:
    return {
        "status": "online",
        "docs": "/docs",
        "mensagem": "API de Foco e Produtividade em execução.",
    }


@app.post(
    "/registro-foco",
    response_model=RegistroFocoResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_registro_foco(payload: RegistroFocoCreate) -> dict:
    """Registra uma sessão de foco recém-finalizada."""
    record = preparar_registro(payload)
    saved_record = insert_focus_record(record)
    return formatar_registro(saved_record)


@app.get(
    "/diagnostico-produtividade",
    response_model=DiagnosticoProdutividadeResponse,
)
def diagnostico_produtividade() -> dict:
    """Gera um resumo inteligente com base em todos os registros salvos."""
    return gerar_diagnostico()
