from datetime import timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.db import get_db
from schemas.index import UserModel, Token
from models.index import User
from sqlalchemy.orm import Session
from config.db import Base, engine
from repository.index import UserRepository
from typing_extensions import Annotated

user = APIRouter()

Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@user.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
) -> Token:
    # TODO: need to add authenticate_user method
    user = authenticate_user(
        db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    # TODO: need to add create_access_token
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@user.get("/", response_model=List[UserModel])
async def read_data(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db),):
    users = db.query(User).all()
    return users


@user.get("/{id}", response_model=List[UserModel])
async def read_data_from_id(id: int, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.id == id)
    return users


@user.post("/users", response_model=UserModel)
async def write_data(user: UserModel, db: Session = Depends(get_db)):
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@user.put("/users/{email}", response_model=UserModel)
async def update_data(email: str, user: UserModel, db: Session = Depends(get_db)):
    updated_user_info = UserRepository.update_user(email, db, user)
    return updated_user_info


@user.delete("/users/{email}", response_model=UserModel)
async def delete_data(email: str, db: Session = Depends(get_db)):
    print(email)
    requested_user = db.query(User).filter(User.email == email)
    if not requested_user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    requested_user.delete()
    db.commit()
    return db.query(User).filter(User.email == email).first()


# @user.get("/{id}")
# async def read_data(id: int):
#     return conn.execute(users.select().where(users.c.id == id)).fetchall()


# @user.post("/")
# async def write_data(user: User):
#     conn.execute(users.insert().values(username=user.name,
#                  email=user.email, password=user.password))
#     return conn.execute(users.select()).fetchall()


# @user.put("/{id}")
# async def update_data(id: int, user: User):
#     conn.execute(users.update().values(username=user.username,
#                  email=user.email, password=user.password))
#     return conn.execute(user.select()).fetchall()


# @user.delete("/{id}")
# async def delete_data(id: int):
#     conn.execute(users.delete().where(users.c.id == id))
#     return conn.execute(users.select()).fetchall()
