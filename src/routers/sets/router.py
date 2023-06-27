from typing import List

from fastapi import APIRouter

from .models import Set

router = APIRouter(prefix="/api/sets", tags=["Sets"])


@router.get("")
def get_sets() -> List[Set]:
    return [
        {"code": "KTK", "name": "Khans of Tarkir"},
        {"code": "DOM", "name": "Dominaria"},
    ]
