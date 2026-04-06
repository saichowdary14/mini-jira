from fastapi import FastAPI
from .routers import user,seed,project,task
from .database import engine,Base
app=FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(user.router)
app.include_router(seed.router)
app.include_router(project.router)
app.include_router(task.router)