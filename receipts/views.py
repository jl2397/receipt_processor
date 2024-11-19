from decimal import Decimal
from math import ceil

from fastapi import APIRouter, HTTPException, status
from . import schemas
import uuid
from datetime import datetime, time

router = APIRouter(prefix="/receipts")

receipt_table = {}

@router.get(path="/{id}/points",
            summary="Returns the points awarded for the receipt",
            description="Returns the points awarded for the receipt",
            response_model=schemas.GetReceiptResponse,
            responses={
                status.HTTP_404_NOT_FOUND: {
                    "description": "No receipt found for that id"
                },
                status.HTTP_200_OK: {
                    "description": "The number of points awarded"
                }
            })
def get_points(id: uuid.UUID) -> schemas.GetReceiptResponse:
    if id not in receipt_table:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Receipt with id {id} not found")
    return schemas.GetReceiptResponse(points=receipt_table[id])


@router.post(path="/process",
             summary="Submits a receipt for processing",
             description="Submits a receipt for processing",
             response_model=schemas.PostReceiptResponse,
             responses={
                status.HTTP_400_BAD_REQUEST: {
                    "description": "The receipt is invalid"
                },
                status.HTTP_201_CREATED: {
                    "description": "Returns the ID assigned to the receipt"
                }
            },
             status_code=status.HTTP_201_CREATED)
def post_receipt(receipt: schemas.Receipt) -> schemas.PostReceiptResponse:
    try:
        receipt_id = process_receipt(receipt)
        return schemas.PostReceiptResponse(id=receipt_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    


def process_receipt(receipt: schemas.Receipt):
    points = 0
    # one point for every alphanumeric character in retailer name
    alphanumeric_chars = [char for char in receipt.retailer if char.isalnum()]
    points += len(alphanumeric_chars)

    # 50 points if the total is a round dollar amount with no cents.
    if receipt.total % 1 == 0:
        points += 50

    # 25 points if the total is a multiple of 0.25.
    if receipt.total % Decimal(".25") == 0:
        points += 25
    
    # 5 points for every two items on the receipt.
    num_items = len(receipt.items)
    points += 5 * (num_items // 2)

    # If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
    for item in receipt.items:
        trimmed_description = item.shortDescription.strip()
        if len(trimmed_description) % 3 == 0:
            points += ceil(item.price * Decimal("0.2"))
        

    # 6 points if the day in the purchase date is odd.
    purchase_date = datetime.strptime(receipt.purchaseDate, "%Y-%m-%d")
    if purchase_date.day % 2 == 1:
        points += 6

    # 10 points if the time of purchase is after 2:00pm and before 4:00pm
    purchase_time = datetime.strptime(receipt.purchaseTime, "%H:%M")

    if purchase_time.time() > time(hour=14, minute=0) and purchase_time.time() < time(hour=18, minute=0):
        points += 10

    receipt_id = uuid.uuid4()
    receipt_table[receipt_id] = points
    return receipt_id
