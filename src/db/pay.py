from psycopg2.extras import RealDictCursor



class PaymentDB:



    def __init__(self):
        pass

    def insert_payment(self, conn, razor_id, user_id, payment):

        query = """
            INSERT INTO payments (razor_id, booking_id, user_id, amount, descriptions, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """

        with conn.cursor(cursor_factory = RealDictCursor) as cursor:

            cursor.execute(
                query, (
                    razor_id,
                    payment.booking_id,
                    user_id,
                    payment.amount,
                    payment.desc,
                    "created"))
            result = cursor.fetchone()

            return result
        

    def get_razor_ids(self, conn, status):

        query = """
            SELECT
                id, razor_id
            FROM payments
            WHERE status = %s
        """

        with conn.cursor(cursor_factory = RealDictCursor) as cursor:

            cursor.execute(query, (status,))
            result = cursor.fetchall()
            return result
        

    def update_status(self, razor_id, status, conn):
        
        query = """
        UPDATE payments
        SET status = %s
        WHERE razor_id = %s
        RETURNING id
        """

        with conn.cursor(cursor_factory = RealDictCursor) as cursor:

            cursor.execute(query, (razor_id, status,))
            result = cursor.fetchone()
            return result
        

    def fetch_status_by_booking_id(self, conn, booking_id):

        query = """
            SELECT
                id, status
            FROM payments
            WHERE booking_id = %s
        """

        with conn.cursor(cursor_factory = RealDictCursor) as cursor:

            cursor.execute(query, (booking_id, ))
            result = cursor.fetchone()
            return result
            