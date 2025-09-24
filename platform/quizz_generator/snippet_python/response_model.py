from pydantic import BaseModel

"""
Modèles Pydantic pour les snippets de code et les batches de snippets.
Ce modèle est envoyé à l'API OpenAI pour création de la réponse."""


class SnippetModel(BaseModel):
    language: str
    level: str
    theme: str
    snippet: str
    choices: list[str]
    answer_id: int
    explanation: str


class SnippetBatch(BaseModel):
    snippets: list[SnippetModel]
