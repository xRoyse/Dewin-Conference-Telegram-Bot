from dataclasses import dataclass
from typing import Optional, List

@dataclass
class GroupUpdate:
    group_id: int
    title: Optional[str] = None
    welcome_message: Optional[str] = None
    farewell_message: Optional[str] = None
    night_mode_enabled: Optional[bool] = None
    night_mode_start: Optional[str] = None
    night_mode_end: Optional[str] = None
    antispam_enabled: Optional[bool] = None
    antispam_threshold: Optional[int] = None
    banned_words: Optional[List[str]] = None
    link_filter_enabled: Optional[bool] = None
    link_whitelist: Optional[List[str]] = None
    language: Optional[str] = None
    avatar_url: Optional[str] = None