from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db_session, get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter(prefix="/api/v1/users", tags=["users"])

def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    if not current_user.get("is_admin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="管理员权限required")
    return current_user

@router.get("/", response_model=List[UserResponse])
def list_users(
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db_session)
):
    users = db.query(User).order_by(User.created_at.desc()).all()
    return users

@router.get("/me", response_model=UserResponse)
def get_me(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db_session)):
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    update: UserUpdate,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db_session)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if update.is_admin is not None:
        user.is_admin = update.is_admin
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db_session)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.username == "admin":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete admin user")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}