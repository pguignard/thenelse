from pydantic import BaseModel
from enum import Enum

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


class Levels(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"


class Languages(Enum):
    PYTHON = "Python"
    JAVASCRIPT = "JavaScript"
    TYPESCRIPT = "TypeScript"
    JAVA = "Java"
    C = "C"
    CSHARP = "C#"
    CPP = "C++"
    GO = "Go"
    PHP = "PHP"
    RUST = "Rust"


class SnippetParams(BaseModel):
    language: Languages
    level: Levels
    theme: str
