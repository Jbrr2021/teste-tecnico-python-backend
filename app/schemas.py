from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class RegistroFocoCreate(BaseModel):
    nivel_foco: int = Field(
        ..., ge=1, le=5, description="1 = muito distraído | 5 = estado de flow"
    )
    tempo_minutos: int = Field(..., gt=0, description="Duração da sessão em minutos")
    comentario: str = Field(..., min_length=3, max_length=500)
    categoria: str = Field(default="geral", min_length=2, max_length=50)
    tags: list[str] = Field(default_factory=list)
    data: Optional[datetime] = Field(
        default=None, description="Data/hora opcional da sessão. Se omitida, usa o momento atual."
    )

    @field_validator("comentario", "categoria")
    @classmethod
    def remover_espacos_extras(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("O campo não pode ficar vazio.")
        return value

    @field_validator("tags")
    @classmethod
    def normalizar_tags(cls, tags: list[str]) -> list[str]:
        tags_limpas = []
        for tag in tags:
            tag_formatada = tag.strip().lower().replace(" ", "-")
            if tag_formatada and tag_formatada not in tags_limpas:
                tags_limpas.append(tag_formatada)
        return tags_limpas


class RegistroFocoResponse(BaseModel):
    id: int
    nivel_foco: int
    tempo_minutos: int
    comentario: str
    categoria: str
    tags: list[str]
    data_registro: datetime

    model_config = ConfigDict(from_attributes=True)


class DiagnosticoProdutividadeResponse(BaseModel):
    total_registros: int
    media_nivel_foco: float
    tempo_total_focado: int
    tempo_total_formatado: str
    percentual_sessoes_flow: float
    categoria_mais_produtiva: Optional[str]
    mensagem_feedback: str
    insight_comentarios: Optional[str]
