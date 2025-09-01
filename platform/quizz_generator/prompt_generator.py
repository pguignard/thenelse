from random import random
from pydantic import BaseModel, Field

from quizz_generator.data.poc_data import get_random_theme

__all__ = ["generate_prompt"]

base_prompt = """
Tu es un créateur de quiz techniques, destinés à s'entraîner et à s'évaluer sur la lecture de code.
L'objectif est de créer des "snippets" (0 à 20 lignes) qui mettent en évidence un concept ou une fonctionnalité spécifique, et dont il faut deviner la sortie.

Paramètres :
- Langage : {LANGUAGE}
- Niveau : {LEVEL}
- Thème : {THEME}

Règles du snippet :
- Court, autonome, exécutable tel quel (print unique).
- Déterministe, pas d’I/O, pas de hasard ni dépendances.
- Montre le thème choisi de façon claire (0–10 lignes débutant, 0–25 confirmé/expert).
- Noms de variables neutres (pas d’indices).

Règles des réponses :
- 4 propositions différentes (A–D), une seule correcte.
- Si exécution normale → sortie exacte.
- Si exception → uniquement le nom du type (ex: "ZeroDivisionError").
- Les mauvaises réponses restent plausibles.
- Explication en Markdown (≈500 caractères ±50%), claire et concise.

Sortie attendue : uniquement un JSON valide, sans texte additionnel, de la forme :
[
{{
  "language": "{LANGUAGE}",
  "level": "{LEVEL}",
  "theme": "{THEME}",
  "snippet": "CODE ICI",
  "choices": ["SORTIE1", "SORTIE2", "SORTIE3", "SORTIE4"],
  "answer_id": 0,
  "explanation": "..."
}},
{{...}}
]

Rappels machine :
- Générer {SNIPPETS_COUNT} snippets.
- Respecter strictement le JSON (guillemets doubles, pas de commentaires).
- Échapper correctement les caractères spéciaux dans "snippet" et "text".
"""


class PromptData(BaseModel):
    language: str = Field(
        ..., description="Le langage de programmation utilisé dans le snippet"
    )
    level: str = Field(..., description="Le niveau de difficulté du snippet")
    theme: str = Field(..., description="Le thème abordé par le snippet")
    snippet_count: int = Field(..., description="Le nombre de snippets à générer")


def get_data() -> PromptData:
    level, theme = get_random_theme()
    return PromptData(
        language="Python",
        level=level,
        theme=theme,
        snippet_count=5,
    )


def generate_prompt(data: PromptData) -> str:
    return base_prompt.format(
        LANGUAGE=data.language,
        LEVEL=data.level,
        THEME=data.theme,
        SNIPPETS_COUNT=data.snippet_count,
    )
