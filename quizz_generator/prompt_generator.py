from random import random
from pydantic import BaseModel, Field
from data.poc_data import poc_data

base_prompt = """
Tu es un générateur d'exercices pour Thenelse.
Objectif : crée un exercice "snippet : guess the output".

Paramètres :
- Langage : {LANGUAGE}   (ex: Python, JavaScript, C, Java, PHP…)
- Niveau : {LEVEL}     (ex: débutant, confirmé, expert)
- Thème : {THEME}       (ex: portée des variables, boucles, closures, arithmétique, immutabilité…)
- Longueur : {LENGTH} lignes environ

Exigences du snippet :
- Court, autonome, exécutable tel quel.
- Déterministe ; aucune dépendance externe ; pas d'horloge, pas de hasard.
- Affiche exactement UNE sortie claire (idéalement une seule ligne) via un print
- Évite les comportements indéfinis/UB.
- Doit illustrer le thème choisi de façon non triviale mais compréhensible.
- Peut être purement éducatif (ex: démonstration de concepts) ou ressemblant à un cas d'utilisation réel.
- Les noms de variables ne doivent pas aider à trouver la réponse.

Exigences des réponses :
- 4 propositions **toutes différentes** et plausibles (A, B, C, D).
- **Une seule** correcte.
- Même si ce n'est pas le thème, le programme peut lever une exception, afin de s'exercer à détecter les bugs
- Si le programme termine normalement → la réponse correcte est la sortie exacte.
- Si le programme lève une exception → la réponse correcte est **strictement le nom du type d'exception** (ex: "ZeroDivisionError"), sans message ni stacktrace.
- Les propositions sont **uniquement** la sortie du programme (pas d'explications).
- L'explication (≤ 300 caractères) justifie **pourquoi** la bonne réponse est correcte (et/ou pourquoi les autres sont fausses), sans verbiage.

Instructions à respecter **ABSOLUMENT** :
- Génère {SNIPPETS_COUNT} snippets différents
- La longueur du snippet doit être de {LENGTH} lignes (+ ou - 30%).
- L'explication doit être de 500 caractères (+ ou - 50%)
- L'explication est formatée en Markdown, avec des `code-block` si besoin, mais sans blockquote

⚠️ Sortie attendue : **UNIQUEMENT** un JSON valide, sans markdown, sans texte additionnel, suivant exactement ce schéma :
[
{{
  "language": "{LANGUAGE}",
  "level": "{LEVEL}",
  "theme": "{THEME}",
  "length": {LENGTH},
  "snippet": "CODE ICI",
  "choices": [
    "SORTIE_POSSIBLE_1",
    "SORTIE_POSSIBLE_2",
    "SORTIE_POSSIBLE_3",
    "SORTIE_POSSIBLE_4"
  ],
  "answer_id": 0,
  "explanation": "...",
}},
{{...}},
etc...
]

Rappels machine :
- Respecter strictement le JSON (guillemets doubles, pas de commentaires).
- Échapper correctement les caractères spéciaux dans "snippet" et "text".
- Ne rien ajouter en dehors de l’objet JSON.
"""


class PromptData(BaseModel):
    language: str = Field(
        ..., description="Le langage de programmation utilisé dans le snippet"
    )
    level: str = Field(..., description="Le niveau de difficulté du snippet")
    theme: str = Field(..., description="Le thème abordé par le snippet")
    length: int = Field(..., description="La longueur du snippet en lignes")
    snippet_count: int = Field(..., description="Le nombre de snippets à générer")


get_random_theme = lambda: random.choice(poc_data["themes"])

data = PromptData(
    language="Python",
    level="débutant",
    theme=get_random_theme(),
    length=2,
    snippet_count=5,
)


def generate_prompt(data: PromptData) -> str:
    return base_prompt.format(
        LANGUAGE=data.language,
        LEVEL=data.level,
        THEME=data.theme,
        LENGTH=data.length,
        SNIPPETS_COUNT=data.snippet_count,
    )


print(generate_prompt(data))
