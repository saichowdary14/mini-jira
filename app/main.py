import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from .routers import user,seed,project,task,comments,activity
from .database import engine,Base
app=FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(user.router)
app.include_router(seed.router)
app.include_router(project.router)
app.include_router(task.router)
app.include_router(comments.router)
app.include_router(activity.router)