import os
import razorpay
from src.db.pay import PaymentDB




payment_db = PaymentDB()

class RazorPaymentGateway:



    def __init__(self):

        self.payment_key = os.getenv("RAZOR_KEY")
        self.payment_secret = os.getenv("RAZOR_SECRET")
        print(f"creds: {self.payment_secret} {self.payment_key}")
        self.client = razorpay.Client(auth=(self.payment_key, self.payment_secret))


    def create_payment(self, user_id, name, email, mobile, payment, conn):

        """
            Docstr
        """

        multiplier = 100
        created_payment = self.client.payment_link.create({
            "amount": payment.amount * multiplier,
            "currency": "INR",
            "description": payment.desc,
            "reference_id": str(payment.booking_id),
            "customer": {
                "name": name,
                "email": email,
                "contact": mobile
            },
            "notify": {
                "sms": False,
                "email": False
            }
        })

        print(f"payment created: {created_payment}")
        print(f"inserting payment data into payment table...")
        db_response = payment_db.insert_payment(
            user_id= user_id,
            payment= payment,
            conn = conn
            )

        result = {
            "payment_id": db_response.get("id"),
            "razor_id": created_payment.get("id"),
            "payment_link": created_payment.get("short_url")
        }

        return result


    def check_payment_details(self, link_id):

        payment_link = self.client.payment_link.fetch(link_id)
        print(f"payment link: {payment_link}")
        return payment_link.get("status")