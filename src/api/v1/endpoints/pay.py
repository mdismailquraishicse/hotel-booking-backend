import traceback
from src.db.session import get_db
from src.core.utils import token_required
from src.services.pay import RazorPaymentGateway
from src.schemas.pydantic_models import Payment
from fastapi import APIRouter, Depends, Request



router = APIRouter()
payment_gateway = RazorPaymentGateway()


@router.post("/create-payment-link")
@token_required
def create_payment_link(request: Request, payment:Payment, conn=Depends(get_db)):

    try:
        payment_link = payment_gateway.create_payment(
            user_id= request.state.user_id,
            name= request.state.fullname,
            email= request.state.email,
            mobile=request.state.mobile,
            payment=payment,
            conn=conn)
        
        conn.commit()

        return {
            "status": "success",
            "result": payment_link,
            "error": None,
            "message": "Payment link created successfully"
        }
    except Exception as e:

        print(f"exception occured: {e}")
        return {
            "status": "failed",
            "result": None,
            "error": traceback.format_exc(),
            "message": str(e)
        }


@router.get("/check-payment-status/{link_id}")
def check_payment_status(link_id):

    try:

        status = payment_gateway.check_payment_details(link_id)
        return {
            "status": "success",
            "result": status,
            "error": None,
            "message": "Payment status fetched successfully"
        }
    except Exception as e:

        print(f"Exception occured: {e}")
        return {
            "status": "failed",
            "result": None,
            "error": traceback.format_exc(),
            "message": str(e)
        }