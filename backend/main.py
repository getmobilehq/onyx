from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes_auth import router as auth_router
from routes_buildings import router as buildings_router
from routes_assessment_items import router as assessment_items_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(buildings_router)
app.include_router(assessment_items_router)

@app.get("/")
def read_root():
    return {"message": "ONYX API running"}
