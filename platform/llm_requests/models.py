from typing import Optional
from pydantic import BaseModel


class ResponseInfo(BaseModel):
    model: str = ""
    temperature: float = 0.0
    service_tier: str = ""
    input_tokens: int = 0
    cached_tokens: int = 0
    output_tokens: int = 0
    reasoning_tokens: int = 0


class CostInfo(BaseModel):
    input_cost: float = 0.0
    output_cost: float = 0.0
    reasoning_cost: float = 0.0
    reasoning_percent: float = 0.0
    total_cost: float = 0.0


class RequestInfo(BaseModel):
    request_name: str = ""
    timestamp: str = ""
    prompt: str = ""
    response_content: str = ""
    response_info: Optional[ResponseInfo] = None
    cost_info: Optional[CostInfo] = None
