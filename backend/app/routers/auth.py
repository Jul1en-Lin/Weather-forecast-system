from fastapi import APIRouter, Request, Response, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db_session, get_current_user
from app.models.user import User
from app.core.security import hash_password, verify_password, create_session, delete_session
from app.schemas.auth import LoginRequest, LoginResponse, MeResponse

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, response: Response, db: Session = Depends(get_db_session)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    session_id = create_session(user.id, user.username)
    response.set_cookie(key="session_id", value=session_id, httponly=True, samesite="lax", path="/")
    return LoginResponse(username=user.username)

@router.post("/logout")
def logout(response: Response, request: Request):
    session_id = request.cookies.get("session_id")
    if session_id:
        delete_session(session_id)
    response.delete_cookie(key="session_id", path="/")
    return {"detail": "Logged out"}

@router.get("/me", response_model=MeResponse)
def me(current_user: dict = Depends(get_current_user)):
    return MeResponse(username=current_user["username"])
