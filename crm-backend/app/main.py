from fastapi import FastAPI
from app.database import Base, engine

from app.models.lead import Lead
from app.models.user import User

from app.routes.webhook import router as webhook_router
from app.routes.leads import router as leads_router
from app.routes.auth import router as auth_router

app = FastAPI(title="CRM 8April")

Base.metadata.create_all(bind=engine)

app.include_router(webhook_router, prefix="/api")
app.include_router(leads_router, prefix="/api")
app.include_router(auth_router, prefix="/api")