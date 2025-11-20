from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .database import engine, Base
from .config import settings, create_upload_dirs
from .api import auth, users, cvs, offers

# Create FastAPI app
app = FastAPI(
    title="SmartHire API",
    description="API pour l'analyse de CV et le matching d'offres d'emploi",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✓ Database tables created")

# Create upload directories
print("Creating upload directories...")
create_upload_dirs()

# Mount static files
try:
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")
    print(f"✓ Static files mounted at /uploads")
except Exception as e:
    print(f"Warning: Could not mount static files: {e}")

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(cvs.router)
app.include_router(offers.router)

# Root endpoint
@app.get("/")
def root():
    return {"message": "SmartHire API v1.0"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Startup event
@app.on_event("startup")
async def startup_event():
    print("\n" + "="*50)
    print("🚀 SmartHire API Started")
    print("="*50)
    print(f"📚 Documentation: http://localhost:8080/docs")
    print(f"🔍 Alternative docs: http://localhost:8080/redoc")
    print(f"💾 Database: {settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else 'configured'}")
    print("="*50 + "\n")
