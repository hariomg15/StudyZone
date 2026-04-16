from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, *, name: str, email: str, hashed_password: str, role):
    try:
        user = User(
            name=name,
            email=email,
            password=hashed_password,
            role=role,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        raise

