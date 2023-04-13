from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    
class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    
    class Config:
        orm_mode = True
        
        
class SubtaskBase(BaseModel):
    title: str
    
class SubtaskCreate(SubtaskBase):
    pass

class Subtask(SubtaskBase):
    id: int
    task_id: int
    
    class Config:
        orm_mode = True