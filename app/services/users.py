from repository.users import UserRepo
from schemas.user import UserPydant, UserUpdatePydant
from models.user import UserDB
from datetime import datetime, timedelta


class UserService:
    def __init__(self, db) -> None:
        self.repo = UserRepo(db=db)

    def get_all_users(self) -> list[UserPydant]:
        all_todos_from_db = self.repo.get_all()  # list[TodoDB]
        # converting sql alchemy models to pydantic models
        result = [UserPydant.from_orm(item) for item in all_todos_from_db]
        return result

    def create_new(self, todo_item: UserPydant) -> UserPydant:
        new_user_from_db = self.repo.create(todo_item)
        return UserPydant.from_orm(
            new_user_from_db
        )  # unpacking sql alchemy model to pydantic model

    def get_by_id(self, id) -> UserPydant:
        user = self.repo.get_by_id(id)
        return UserPydant.from_orm(user)

    def update_existing(self, id: int, todo_item: UserUpdatePydant) -> UserUpdatePydant:
        updated_user_from_db = self.repo.update_existing_db(id, todo_item)
        return updated_user_from_db

    def delete_by_id(self, id):
        self.repo.delete(id)

    def search(self, query):
        return self.repo.search_db(query)

    def get_upcoming_birthdays(self):
        now = datetime.now()
        next_year = now.replace(year=now.year + 1)
        end_date = max(now + timedelta(days=7), next_year)
        return self.repo.get_upcoming_birthdays(end_date)
