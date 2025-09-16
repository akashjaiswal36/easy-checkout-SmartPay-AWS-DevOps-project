from fastapi import FastAPI, HTTPException
from uuid import uuid4
import boto3
import json
import logging



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

@app.get("/")
def health_check():
    return {"status": "SmartPay is healthy"}


def get_api_key():
    client = boto3.client("secretsmanager", region_name="ap-south-1")
    response = client.get_secret_value(SecretId="smartpay/api-key")
    secret = json.loads(response["SecretString"])
    return secret["API_KEY"]

@app.get("/apikey")
def show_api_key():
    return {"api_key": get_api_key()}


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

@app.post("/pay")
def pay(amount: float, method: str):
    txn_id = str(uuid.uuid4())
    transactions[txn_id] = {"amount": amount, "method": method, "status": "success"}
    logger.info(f"Payment processed | txn_id={txn_id} | amount={amount} | method={method}")
    return {"transaction_id": txn_id, "status": "success"}
