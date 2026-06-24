from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from . import models
from .routers import auth, citizens, announcements, reports, requests, services
from .routers import emergencies, wifi, youth, projects, messages, documents, sms, ai, analytics

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Umudugudu Digital Platform API",
    version="1.0.0",
    description="REST API for village digital management system - 15 modules"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(auth.router)
app.include_router(citizens.router)
app.include_router(announcements.router)
app.include_router(reports.router)
app.include_router(requests.router)
app.include_router(services.router)
app.include_router(emergencies.router)
app.include_router(wifi.router)
app.include_router(youth.router)
app.include_router(projects.router)
app.include_router(messages.router)
app.include_router(documents.router)
app.include_router(sms.router)
app.include_router(ai.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {"message": "Welcome to Umudugudu Digital Platform", "version": "1.0.0", "modules": 15}

@app.get("/health")
def health():
    return {"status": "ok"}
