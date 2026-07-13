from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database_config import get_db
from payment_repository import PaymentRepository
from resp_models import PaymentInitializeSchema, PaymentCompleteSchema

router = APIRouter()


@router.post("/initialize", status_code=status.HTTP_201_CREATED)
async def initialize_new_payment(
        payload: PaymentInitializeSchema,
        db: AsyncSession = Depends(get_db)
):
    payment = await PaymentRepository.initialize_payment(
        db=db,
        booking_id=payload.booking_id,
        amount=payload.amount,
        method=payload.method
    )
    return {"status": "success", "data": payment}


@router.patch("/{payment_id}/complete", status_code=status.HTTP_200_OK)
async def complete_existing_payment(
        payment_id: int,
        payload: PaymentCompleteSchema,
        db: AsyncSession = Depends(get_db)
):
    updated_payment = await PaymentRepository.complete_payment(
        db=db,
        payment_id=payment_id,
        transaction_id=payload.transaction_id
    )

    if not updated_payment:
        raise HTTPException(status_code=404, detail="Payment record not found")

    return {"status": "success", "message": "Payment completed and booking confirmed", "data": updated_payment}