from pydantic import BaseModel
from typing import List

class GroupSettingsUpdate(BaseModel):
    group_id: int
    night_mode: bool | None = None
    anti_spam: bool | None = None
    language: str | None = None

class GroupSettingsOut(BaseModel):
    group_id: int
    title: str
    avatar_url: str
    night_mode: bool
    anti_spam: bool
    language: str

class GroupSettingsResponse(BaseModel):
    is_premium: bool
    groups: List[GroupSettingsOut]