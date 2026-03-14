#app/main.py
# FastAPI
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import Base, engine, SessionLocal
from app import models, schemas

app = FastAPI()

# create tables
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "FastAPI is running 🚀"}


@app.post("/items", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(
        name=item.name,
        description=item.description
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


@app.get("/items", response_model=list[schemas.ItemResponse])
def get_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()


# --- Users endpoint ---
@app.post("/users", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
