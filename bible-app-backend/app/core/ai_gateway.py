"""AI Gateway wrapping Ollama API for Bible study questions."""
import logging

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "Voce e um assistente de estudo biblico. "
    "Responda em portugues de forma clara e concisa. "
    "Baseie-se em fatos historicos, contexto cultural e linguistico. "
    "NAO crie interpretacoes doutrinarias. "
    "NAO invente informacoes. Se nao souber, diga que nao sabe. "
    "Limite sua resposta a no maximo 300 palavras."
)


async def ask_ollama(
    verse_ref: str,
    verse_text: str,
    question: str,
) -> str:
    """Send a question about a Bible verse to Ollama and return the answer.

    Args:
        verse_ref: e.g. "Joao 3:16 (NVI)"
        verse_text: the actual verse text
        question: user's question

    Returns:
        The AI-generated answer string.

    Raises:
        httpx.HTTPError: if Ollama is unreachable or returns an error.
    """
    prompt = (
        f"Versiculo: {verse_ref}\n"
        f'Texto: "{verse_text}"\n\n'
        f"Pergunta do usuario: {question}"
    )

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{settings.OLLAMA_URL}/api/generate",
            json={
                "model": settings.OLLAMA_MODEL,
                "system": SYSTEM_PROMPT,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "num_predict": 512,
                },
            },
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()
