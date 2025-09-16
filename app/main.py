from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import uuid
import boto3
import json
import logging
import os

app = FastAPI()
transactions = {}
templates = Jinja2Templates(directory="app/templates")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

@app.get("/")
def health_check():
    return {"status": "SmartPay is healthy"}

@app.post("/pay")
def make_payment(amount: float, method: str = "card"):
    txn_id = str(uuid.uuid4())
    transactions[txn_id] = {"amount": amount, "method": method, "status": "success"}
    logger.info(f"Payment processed | txn_id={txn_id} | amount={amount} | method={method}")
    return {"transaction_id": txn_id, "status": "success"}

@app.get("/status/{txn_id}")
def check_status(txn_id: str):
    txn = transactions.get(txn_id)
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return txn

@app.get("/apikey")
def show_api_key():
    try:
        client = boto3.client("secretsmanager", region_name="ap-south-1")
        response = client.get_secret_value(SecretId="smartpay/api-key")
        secret = json.loads(response["SecretString"])
        return {"api_key": secret.get("API_KEY", "not-set")}
    except Exception as e:
        logger.error(f"Error fetching API key: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve API key")

@app.get("/payform", response_class=HTMLResponse)
def get_form(request: Request):
    return templates.TemplateResponse("payform.html", {"request": request})

@app.post("/payform", response_class=HTMLResponse)
def submit_form(request: Request, amount: float = Form(...), method: str = Form(...)):
    txn_id = str(uuid.uuid4())
    transactions[txn_id] = {"amount": amount, "method": method, "status": "success"}
    logger.info(f"Form payment | txn_id={txn_id} | amount={amount} | method={method}")
    return HTMLResponse(content=f"<h3>Payment Successful!</h3><p>Transaction ID: {txn_id}</p>", status_code=200)