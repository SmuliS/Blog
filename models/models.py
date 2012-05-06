from sqlalchemy import Column, Integer, String, Text
from database import Base


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(String(30), unique=False)
    text = Column(Text(260), unique=False)
    tags = Column(String(30), unique=False)

    def __init__(self, title=None, text=None, tags=None):
        self.title = title
        self.text = text
        self.tags = tags

    def __repr__(self):
        return '<Post %r>' % self.title
