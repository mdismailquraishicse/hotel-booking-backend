from fastapi import APIRouter
from src.services.pay import RazorPaymentGateway
from src.schemas.pydantic_models import Payment



router = APIRouter()
rpg = RazorPaymentGateway()


@router.post("/create-payment-link")
def create_payment_link(payment:Payment):

    return rpg.create_payment(payment=payment)

