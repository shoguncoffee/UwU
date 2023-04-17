from typing import Union

from fastapi import FastAPI

from ..spawn import aircraft

app = FastAPI()


aircrafts = [aircraft]


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
