from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.models import get_db
from app.services.auth import (
    authenticate_user,
    create_access_token,
)


auth_route = APIRouter(
    prefix="/auth",
    tags=["authentication", "authoriation"],
    responses={"404": {"description": "Not found."}}
)


@auth_route.post("/token", status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db),
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=404, detail="No Valid User.")
    token_expires = timedelta(minutes=60 * 24 * 3)  # 3 days valid token
    token = create_access_token(
        user.username,
        user.id,
        # user.admin,
        expires_delta=token_expires
    )
    return {"token": token}
