from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any

from app.database import list_focus_records
from app.schemas import RegistroFocoCreate


DISTRACTION_KEYWORDS = {
    "celular": "O celular apareceu como possível distração. Teste deixá-lo longe durante blocos de foco.",
    "whatsapp": "O WhatsApp apareceu como possível distração. Silenciar notificações pode ajudar.",
    "notificação": "Notificações foram citadas. Experimente usar modo foco ou não perturbe.",
    "barulho": "Barulho foi citado. Fone, música ambiente ou troca de local podem melhorar seu foco.",
    "reunião": "Reuniões apareceram nos comentários. Tente separar blocos de execução dos blocos de reunião.",
}


def preparar_registro(payload: RegistroFocoCreate) -> dict[str, Any]:
    """Converte o payload validado para o formato salvo no banco."""
    data_registro = payload.data or datetime.now(timezone.utc)
    return {
        "nivel_foco": payload.nivel_foco,
        "tempo_minutos": payload.tempo_minutos,
        "comentario": payload.comentario,
        "categoria": payload.categoria.lower(),
        "tags": ",".join(payload.tags),
        "data_registro": data_registro.isoformat(),
    }


def formatar_registro(row: dict[str, Any]) -> dict[str, Any]:
    """Converte uma linha do banco para resposta JSON amigável."""
    return {
        **row,
        "tags": [tag for tag in row["tags"].split(",") if tag],
        "data_registro": row["data_registro"],
    }


def gerar_feedback(
    media_foco: float,
    tempo_total: int,
    total_registros: int,
    percentual_flow: float,
) -> str:
    if total_registros == 0:
        return "Ainda não há registros. Faça seu primeiro bloco de foco para gerar um diagnóstico."

    if media_foco < 3:
        mensagem = "Seu foco médio ficou baixo. Sugestão: reduza notificações, faça pausas maiores e use blocos menores de trabalho."
    elif media_foco <= 4:
        mensagem = "Sua produtividade está razoável, mas pode melhorar com blocos mais consistentes e menos interrupções."
    else:
        mensagem = "Ótimo nível de foco! Continue mantendo o ritmo com pausas saudáveis e proteção dos seus blocos."

    if tempo_total >= 240 and media_foco >= 4:
        mensagem += " Como você acumulou bastante tempo focado, lembre-se de fazer pausas para evitar queda de energia."

    if percentual_flow >= 60:
        mensagem += " A maioria das suas sessões ficou em estado de flow. Excelente sinal de ritmo produtivo."

    return mensagem


def detectar_insight_comentarios(comentarios: list[str]) -> str | None:
    texto = " ".join(comentarios).lower()
    for palavra, insight in DISTRACTION_KEYWORDS.items():
        if palavra in texto:
            return insight
    return None


def gerar_diagnostico() -> dict[str, Any]:
    registros = list_focus_records()
    total_registros = len(registros)

    if total_registros == 0:
        return {
            "total_registros": 0,
            "media_nivel_foco": 0,
            "tempo_total_focado": 0,
            "tempo_total_formatado": "0h 0min",
            "percentual_sessoes_flow": 0,
            "categoria_mais_produtiva": None,
            "mensagem_feedback": gerar_feedback(0, 0, 0, 0),
            "insight_comentarios": None,
        }

    soma_foco = sum(item["nivel_foco"] for item in registros)
    tempo_total = sum(item["tempo_minutos"] for item in registros)
    media_foco = round(soma_foco / total_registros, 2)

    sessoes_flow = sum(1 for item in registros if item["nivel_foco"] >= 4)
    percentual_flow = round((sessoes_flow / total_registros) * 100, 2)

    tempo_por_categoria: dict[str, int] = defaultdict(int)
    foco_por_categoria: dict[str, list[int]] = defaultdict(list)

    for item in registros:
        categoria = item["categoria"]
        tempo_por_categoria[categoria] += item["tempo_minutos"]
        foco_por_categoria[categoria].append(item["nivel_foco"])

    # Categoria produtiva = melhor equilíbrio entre foco médio e tempo investido.
    pontuacoes = {}
    for categoria, focos in foco_por_categoria.items():
        media_categoria = sum(focos) / len(focos)
        pontuacoes[categoria] = media_categoria * tempo_por_categoria[categoria]

    categoria_mais_produtiva = Counter(pontuacoes).most_common(1)[0][0]
    horas, minutos = divmod(tempo_total, 60)

    comentarios = [item["comentario"] for item in registros]

    return {
        "total_registros": total_registros,
        "media_nivel_foco": media_foco,
        "tempo_total_focado": tempo_total,
        "tempo_total_formatado": f"{horas}h {minutos}min",
        "percentual_sessoes_flow": percentual_flow,
        "categoria_mais_produtiva": categoria_mais_produtiva,
        "mensagem_feedback": gerar_feedback(
            media_foco, tempo_total, total_registros, percentual_flow
        ),
        "insight_comentarios": detectar_insight_comentarios(comentarios),
    }
