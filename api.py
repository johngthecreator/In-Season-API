from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Season(BaseModel):
    currSeason:str

class Produce(BaseModel):
    produce:str

produce_list = []

@app.get("/")
def main():
    return {"status":"api is running"}

@app.post("/season")
def season(season: Season):
    with open('produce.json') as file:
        data = file.read()
        produce = json.loads(data)
        for p in produce:
            if season.currSeason.lower() in p["seasons"]:
                produce_list.append(p["produce"]) 
        return {"status":produce_list}

@app.post("/produce")
def produce(produce: Produce):
    with open('produce.json') as file:
        data = file.read()
        all_produce = json.loads(data)
        for p in all_produce:
            if produce.produce in p["produce"].lower():
                produce_list.append({"in_season":p["seasons"]})
        return {"status":produce_list}