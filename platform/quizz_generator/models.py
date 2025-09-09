from pydantic import BaseModel


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
