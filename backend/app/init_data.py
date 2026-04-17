from app.database import SessionLocal
from app.models.user import User
from app.core.security import hash_password

def init_db():
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == "admin").first()
        if not existing:
            user = User(
                username="admin",
                password_hash=hash_password("admin123"),
            )
            db.add(user)
            db.commit()
            print("Default user created: admin / admin123")
        else:
            print("Default user already exists")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
