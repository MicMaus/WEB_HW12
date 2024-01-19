from models.user import ClientDB
from fastapi import HTTPException


class ClientRepo:
    def get_by_id(self, user_id: str, requesting_user_id: str):
        if requesting_user_id != user_id:
            raise HTTPException(
                status_code=401, detail="Invalid authorization credentials"
            )
        return self.db.query(ClientDB).filter(ClientDB.id == user_id).first()

    def create(self, item):
        new_item = ClientDB(**item.dict())
        self.db.add(new_item)
        self.db.commit()
        self.db.refresh(new_item)
        return new_item
