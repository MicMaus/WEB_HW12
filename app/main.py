from fastapi import (
    FastAPI,
    Query,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session
from sqlalchemy import text
from dependencies.db import get_db, engine
from api.users_routes import router as user_router
from models import user, client
from api.auth_routes import router as auth_router


user.Base.metadata.create_all(bind=engine)
client.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router, prefix="/users")
app.include_router(auth_router, prefix="/clients")


@app.get("/")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Здійснюємо запит
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return "Database is configured correctly"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")
