from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ConferenceSchema(BaseModel):
    title: str
    summary: str
    location: str
    date: Optional[datetime]
    primary_moa: Optional[List[str]]
    primary_product: Optional[str]
    secondary_product: Optional[str]
    conference_source: str = Field(alias="source")
    primary_author: Optional[str]
    secondary_moa: Optional[List[str]]


class ConferenceDataSchema(BaseModel):
    chat_gpt_answer: str
    answer: List[ConferenceSchema]


class ConferenceResponseSchema(BaseModel):
    success: bool
    message: str
    data: ConferenceDataSchema
