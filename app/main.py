from fastapi import FastAPI
from app.database import Base, engine
from app.routers import company_router

app = FastAPI(title="Wanted python assignment API")

Base.metadata.create_all(bind=engine)

app.include_router(company_router.router)
