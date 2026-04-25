import os
import razorpay




class RazorPaymentGateway:



    def __init__(self):

        self.payment_key = os.getenv("RAZOR_KEY")
        self.payment_secret = os.getenv("RAZOR_SECRET")
        print(f"creds: {self.payment_secret} {self.payment_key}")
        self.client = razorpay.Client(auth=(self.payment_key, self.payment_secret))


    def create_payment(self, payment):

        """
            Docstr
        """

        created_payment = self.client.payment_link.create({
            "amount": payment.amount,
            "currency": "INR",
            "description": payment.desc,
            "reference_id": str(payment.booking_id),
            "customer": {
                "name": payment.name,
                "email": payment.email,
                "contact": payment.mobile
            },
            "notify": {
                "sms": False,
                "email": False
            }
        })

        print(f"payment created: {created_payment}")
        return created_payment["short_url"]

