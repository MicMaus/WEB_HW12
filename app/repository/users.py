from models.user import UserDB
from sqlalchemy import or_
from datetime import datetime


class UserRepo:
    def __init__(self, db) -> None:
        self.db = db

    def get_all(self) -> list[UserDB]:
        return self.db.query(UserDB).filter()

    def create(self, todo_item):
        new_item = UserDB(**todo_item.dict())
        self.db.add(new_item)
        self.db.commit()
        self.db.refresh(new_item)
        return new_item

    def get_by_id(self, id):
        return self.db.query(UserDB).filter(UserDB.id == id).first()

    def update_existing_db(self, id: int, todo_item):
        updated_user = self.db.query(UserDB).filter(UserDB.id == id).first()
        # Update user attributes with values from todo_item:
        for key, value in todo_item.dict().items():
            setattr(updated_user, key, value)

        self.db.commit()
        self.db.refresh(updated_user)
        return updated_user

    def delete(self, id):
        user = self.get_by_id(id)
        self.db.delete(user)
        self.db.commit()

    def search_db(self, query):
        query = "%{}%".format(query)
        results = (
            self.db.query(UserDB)
            .filter(
                or_(
                    UserDB.name.ilike(query),
                    UserDB.surname.ilike(query),
                    UserDB.email.ilike(query),
                )
            )
            .all()
        )

        return results

    def get_upcoming_birthdays(self, end_date: datetime):
        return self.db.query(UserDB).filter(UserDB.birthday <= end_date).all()
