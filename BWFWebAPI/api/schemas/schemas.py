from typing import Optional
from pydantic import BaseModel, Field

class PlayerInfo(BaseModel):
    name: str = Field(None, example="Badminton Taro")
    id: int = Field(None, example=12345)
    profile: str = Field(None,example="107BF7B1-96F5-47B4-9764-979F659752A0")
    