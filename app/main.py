from fastapi import FastAPI, HTTPException
from uuid import uuid4

app = FastAPI()
transactions = {}

@app.post("/pay")
def make_payment(amount: float, method: str = "card"):
    txn_id = str(uuid4())
    transactions[txn_id] = {"amount": amount, "method": method, "status": "success"}
    return {"transaction_id": txn_id, "status": "success"}

@app.get("/status/{txn_id}")
def check_status(txn_id: str):
    txn = transactions.get(txn_id)
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return txn