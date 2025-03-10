from fastapi import APIRouter

router = APIRouter()

@router.get("/{property_id}")
def read_property(property_id: int):
    return {"property_id": property_id}
