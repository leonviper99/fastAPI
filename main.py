from fastapi import Depends, FastAPI, HTTPException, Depends, Body, Request, Form, status
from sqlalchemy.orm import Session
from datetime import datetime, time, timedelta, date, timezone
from typing import Annotated
from uuid import UUID
# from . import crud, models, schemas
from starlette.responses import RedirectResponse
from database import sessionLocal, engine
import models
import sys 

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@app.get("/")
async def home(req: Request,  db: Session = Depends(get_db)):
    skip = 0
    limit = 100
    tasks = db.query(models.Task).filter(models.Task.status == False).offset(skip).limit(limit).all()
    return tasks

@app.get("/task_details")
async def task_details(req: Request, task_id: int, db: Session = Depends(get_db)):
    skip = 0
    limit = 100
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        subtasks = db.query(models.Subtask).filter(models.Subtask.task_id == task_id).offset(skip).limit(limit).all()
        return task , """ ------------Subtasks---------- """ , subtasks

@app.post("/add")
async def add_task(req: Request, title: str = Form(...),description: str = Form(...), db: Session = Depends(get_db)):
    new_task = models.Task(title=title, description = description)
    db.add(new_task)
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

@app.get("/done")
async def finished_tasks(req: Request, db: Session = Depends(get_db)):
    skip = 0
    limit = 100
    tasks = db.query(models.Task).filter(models.Task.flag == 1).offset(skip).limit(limit).all()     
    return tasks

@app.get("/deleted")
async def deleted_tasks(req: Request, db: Session = Depends(get_db)):
    skip = 0
    limit = 100
    tasks = db.query(models.Task).filter(models.Task.status == 1).offset(skip).limit(limit).all()        
    return tasks

@app.get("/update/{task_id}")
async def update_task(req: Request, task_id: int | None = None, new_title: str | None = None, complete: bool | None = None, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    skip = 0
    limit = 100
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if complete == 1:
        subtasks = db.query(models.Subtask).filter(models.Subtask.task_id == task_id and models.Subtask.flag == 0 ).offset(skip).limit(limit).all()
        if len(subtasks) > 0:
            raise HTTPException(status_code=409, detail="Subtasks not complete")
    
    else:    
        task.flag = complete
        task.title = new_title
        task.updated_date = datetime.today()
        db.commit()
        url = app.url_path_for("home")
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete/{task_id}")
async def delete_task(req: Request, task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if(task.status == False):
        task.status = not task.status
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

@app.get("/restore/{task_id}")
async def restore_task(req: Request, task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if(task.status == True):
        task.status = not task.status
    db.commit()
    url = app.url_path_for("deleted_tasks")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

@app.get("/subtasks")
async def subtasks(req: Request, db: Session = Depends(get_db)):
    skip = 0
    limit = 100
    subtasks = db.query(models.Subtask).filter(models.Subtask.status == False).offset(skip).limit(limit).all() 
    return subtasks

@app.post("/subtask/add")
async def add_sub_task(req: Request, task_id: int, title: str = Form(...), db: Session = Depends(get_db)):
    new_task = models.Subtask(title = title, task_id = task_id)
    parent = db.query(models.Task).filter(models.Task.id == task_id).first()
    if parent is None:
        raise HTTPException(status_code=404, detail="Parent task not found")
    db.add(new_task)
    db.commit()
    url = app.url_path_for("subtasks")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

@app.get("/subtask/update/{subtask_id}")
async def update_subtask(req: Request, subtask_id: int, new_title: str | None = None, complete: bool | None = None, db: Session = Depends(get_db)):
    subtask = db.query(models.Subtask).filter(models.Subtask.id == subtask_id).first()
    subtask.title = new_title
    subtask.flag = complete
    if subtask is None:
        raise HTTPException(status_code=404, detail="Subtask not found")
    if(subtask.status == False):
        subtask.status = not subtask.status
    db.commit()
    url = app.url_path_for("subtasks")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

@app.get("/subtask/delete/{subtask_id}")
async def delete_subtask(req: Request, subtask_id: int, db: Session = Depends(get_db)):
    subtask = db.query(models.Subtask).filter(models.Subtask.id == subtask_id).first()
    if subtask is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if(subtask.status == False):
        subtask.status = not subtask.status    
    db.commit()
    url = app.url_path_for("subtasks")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

