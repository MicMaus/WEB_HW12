from fastapi import APIRouter, Depends
from schemas.user import UserPydant, UserUpdatePydant
from dependencies.db import get_db, SessionLocal
from services.users import UserService


router = APIRouter()


@router.get("/")
def list_users(db: SessionLocal = Depends(get_db)) -> list[UserPydant]:
    todo_items = UserService(db=db).get_all_users()
    return todo_items


@router.get("/upcoming-birthdays")
def get_upcoming_birthdays(db: SessionLocal = Depends(get_db)):
    return UserService(db).get_upcoming_birthdays()


@router.get("/{id}")
def get_detail(id: int, db: SessionLocal = Depends(get_db)) -> UserPydant:
    todo_item = UserService(db=db).get_by_id(id)
    return todo_item


@router.post("/")
def create_user(
    todo_item: UserPydant, db: SessionLocal = Depends(get_db)
) -> UserPydant:
    new_item = UserService(db=db).create_new(todo_item)
    return new_item


@router.put("/{id}")
def update_user(
    id: int, todo_item: UserUpdatePydant, db: SessionLocal = Depends(get_db)
) -> UserPydant:
    updated_user = UserService(db=db).update_existing(id, todo_item)
    return updated_user


@router.delete("/{id}")
def delete_user(id: int, db: SessionLocal = Depends(get_db)):
    UserService(db=db).delete_by_id(id)
    return f"message: User {id} was deleted"


@router.get("/search/{query}")
# optionally this method can be moved to the top before other methods with "/{id}", in such case {query} can be removed from this decorator. now {query} serves to avoid conflicts
def search_users(query: str, db: SessionLocal = Depends(get_db)):
    return UserService(db).search(query)
