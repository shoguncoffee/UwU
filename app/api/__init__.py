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

'''from src.K.payment import Payment

payment = [Payment]

@app.get("/payment",tags=["payment"])
async def get_payment() -> dict:
    return {"Data": payment}

@app.post("/payment",tags=["payment"])
async def add_payment(transaction_id:str,payment_time:str,status:str) -> dict:
    for payment in payment:
        if transaction_id in payment.transaction_id:
            payment.append(payment)
            return {"Data": "Added"}'''
    