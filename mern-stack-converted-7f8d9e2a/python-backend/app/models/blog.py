from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    desc = Column(String, nullable=False)
    img = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="blogs")

    def __repr__(self):
        return f"<Blog(id={self.id}, title='{self.title}', user_id={self.user_id})>"