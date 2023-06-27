from pydantic import BaseModel, Field
from typing import List


class Set(BaseModel):
    code: str = Field(example="KTK")
    name: str = Field(example="Khans of Tarkir")
