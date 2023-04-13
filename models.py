import sys
import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Text, DateTime, Date
from sqlalchemy.orm import relationship

from database import Base

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, unique = True, index = True)
    description = Column(String, index = True)
    flag = Column(Boolean, default=False)
    status = Column(Boolean, default=False)
    progress = Column(Float, default = 0)
    schedule_date = Column(DateTime)
    created_date = Column(DateTime, default = datetime.datetime.utcnow())
    updated_date = Column(DateTime)
    
    subtodos = relationship("Subtask", back_populates="todo")
    
class Subtask(Base):
    __tablename__ = "subtasks"
    
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, unique = True, index = True)
    flag = Column(Boolean, default=False)
    status = Column(Boolean, default=False)
    task_id= Column(Integer, ForeignKey('tasks.id'))

    todo = relationship("Task", back_populates="subtodos")
    
