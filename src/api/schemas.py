# src/api/schemas.py
from pydantic import BaseModel
from typing import List

class RegionResult(BaseModel):
    label: str
    text: str
    confidence: float

class ConvertResponse(BaseModel):
    markdown: str
    confidence: float
    regions: List[RegionResult]