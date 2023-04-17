from typing import Union

from fastapi import FastAPI

from ..spawn import aircraft,instance


app = FastAPI()


aircrafts = [aircraft]
instances = [instance]
accounts = []

@app.get("/aircrafts",tags=["aircrafts"])
async def get_aircrafts() -> dict:
    return {"Data": aircrafts}

@app.delete("/aircraft/{model}",tags=["aircrafts"])
async def delete_aircraft(model:str) -> dict:
    for aircraft in aircrafts:
        if model in aircraft.model:
            aircrafts.remove(aircraft)
            return {"Data": "Deleted"}
    return {"Data": "Not Found"}

@app.get("/search_flight",tags=["search_flight"])
async def get_flights() -> dict:

    #need to add search flight

    return {"Data": instances} 

@app.post("/account",tags=["account"])
async def add_account(account: dict) -> dict:
    accounts.append(account)
    return {"Data": "Account Added"}

@app.get("/account",tags=["account"])
async def get_account() -> dict:
    return {"Data": accounts} #need to add account