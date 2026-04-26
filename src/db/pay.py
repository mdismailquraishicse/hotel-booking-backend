from psycopg2.extras import RealDictCursor



class PaymentDB:



    def __init__(self):
        pass

    def insert_payment(self, conn, user_id, payment):

        query = """
            INSERT INTO payments (booking_id, user_id, amount, descriptions, status)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """

        with conn.cursor(cursor_factory = RealDictCursor) as cursor:

            cursor.execute(
                query, (
                    payment.booking_id,
                    user_id,
                    payment.amount,
                    payment.desc,
                    "created"))
            result = cursor.fetchone()

            return result
            