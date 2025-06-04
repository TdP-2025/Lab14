from database.DB_connect import DBConnect
from model.arco import Arco
from model.ordine import Ordine
from model.store import Store


class DAO():
    @staticmethod
    def getStores():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select s.*
                    from stores s """

        cursor.execute(query)

        for row in cursor:
            result.append(Store(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getOrdiniStore(store):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select o.*
                    from orders o 
                    where o.store_id = %s"""

        cursor.execute(query, (store, ))

        for row in cursor:
            result.append(Ordine(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi(store, k, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT o1.order_id AS ordine1, o2.order_id AS ordine2, (SELECT SUM(quantity) FROM order_items WHERE order_id = o1.order_id) + (SELECT SUM(quantity) FROM order_items WHERE order_id = o2.order_id) AS peso
                    FROM orders o1, orders o2
                    WHERE o1.store_id = %s
                    AND o2.store_id = %s
                    AND o1.order_id <> o2.order_id
                    AND o1.order_date > o2.order_date
                    AND DATEDIFF(o1.order_date, o2.order_date) < %s"""

        cursor.execute(query, (store, store, k))

        for row in cursor:
            result.append(Arco(idMap[row["ordine1"]], idMap[row["ordine2"]], row["peso"]))

        cursor.close()
        conn.close()
        return result