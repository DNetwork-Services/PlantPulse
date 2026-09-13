from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="PlantPulse API",
    description="Ethanol Plant Operations & Asset Management Platform",
    version="0.1.0",
)

# Allow the local Vite dev server to call this API.
# NEVER use allow_origins=["*"] once real auth/cookies are involved — 
# we'll tighten this per-environment in later phases (dev/staging/prod
# will each have their own explicit allowed origin).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "service": "plantpulse-backend"}


@app.get("/")
def root():
    return {"message": "PlantPulse API is running"}