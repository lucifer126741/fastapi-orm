from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.index import User
from schemas.users import UserModel


class UserRepository:

    @classmethod
    def get_all_users(cls, db: Session):
        return db.query(User).all()

    @classmethod
    def get_user_from_email(cls, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @classmethod
    def add_user(cls, db: Session, user: UserModel):
        new_user = User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @classmethod
    def update_user(cls, email: str, db: Session, user: UserModel):
        requested_user = db.query(User).filter(User.email == email)
        if not requested_user.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        requested_user.update(
            {'username': user.username, 'email': user.email, 'password': user.password})
        db.commit()
        return db.query(User).filter(User.email == user.email)
        # print(dict(user))
        # return {'mesage': 'hello world'}
