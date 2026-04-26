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
            razor_id= created_payment.get("id"),
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
    

    def update_status(self, conn):

        print("getting razor_ids...")
        current_status = "created"
        razor_ids = payment_db.get_razor_ids(conn = conn, status = current_status)
        razor_ids = [row.get("razor_id") for row in razor_ids]
        print(f"razor_ids: {razor_ids}")
        for razor_id in razor_ids:
            status = self.check_payment_details(link_id= razor_id)
            update_response = payment_db.update_status(
                razor_id=razor_id,
                status= status,
                conn= conn)
            if not update_response:
                continue
        print(f"updated all the status")
        return True
            