from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class Document(BaseModel):
    text: str
    metadata: Dict[str, Any] = {}

class SearchQuery(BaseModel):
    query: str
    limit: int = 5
    filter_key: Optional[str] = None
    filter_value: Optional[str] = None

class SearchResult(BaseModel):
    text: str
    metadata: Dict[str, Any]
    score: float