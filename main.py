from fastapi import FastAPI, Depends, Form
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime 
DATABASE_URL = "postgresql://postgres:admin@localhost/comentdb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now())

Base.metadata.create_all(bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        


@app.get("/comments")
async def get_comments(db: Session = Depends(get_db)):
    comments = db.query(Comment).order_by(Comment.created_at.desc()).all()
    return [{"id": c.id, "username": c.username, "content": c.content, "created_at": c.created_at} for c in comments]

@app.post("/add_comment")
async def add_comment(username: str = Form(...), content: str = Form(...), db: Session = Depends(get_db)):
    new_comment = Comment(username=username, content=content)
    db.add(new_comment)
    db.commit()
    return {"id": new_comment.id, "username": new_comment.username, "content": new_comment.content, "created_at": new_comment.created_at}


def test ():
    pass

