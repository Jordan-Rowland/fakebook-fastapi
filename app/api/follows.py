from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models import get_db
from app.models.follows import Follow
from app.services.users import get_current_user


follows_route = APIRouter(
    prefix="/follows",
    tags=["follows"],
    responses={"404": {"description": "Not found."}}
)


@follows_route.get("")
def get_follows(user: dict=Depends(get_current_user), db: Session=Depends(get_db)):
    return db.query(Follow).filter(Follow.follower_id == user["id"]).all()
