from database.DB_connect import DBConnect
from database import Store as s
from database import Arco as a
from database import Ordine as o

class DAO():

    def getStores(self):
        cnx = DBConnect.get_connection()
        if cnx is None:
            print("Connessione fallita.")
        else:
            cursor = cnx.cursor(dictionary = True)

            res = []

            query = "select * from stores"

            cursor.execute(query)

            for row in cursor:
                res.append(s.Store(**row))

            cursor.close()
            cnx.close()

            return res

    def getNodes(self, id_store):
        cnx = DBConnect.get_connection()

        if cnx is None:
            print("Connessione fallita.")
        else:
            cursor = cnx.cursor(dictionary=True)
            res = []

            query = """select *
                    from orders  o
                    where o.store_id = %s"""

            cursor.execute(query, (id_store,))

            for row in cursor:
                res.append(o.Ordine(**row))

            cursor.close()
            cnx.close()

            return res


    def getEdges(self, num_giorni, id_store):
        cnx = DBConnect.get_connection()

        if cnx is None:
            print("Connessione fallita.")
        else:
            cursor = cnx.cursor(dictionary=True)
            res = []

            query = """select o1.order_id as u, o2.order_id as v, sum(oi1.quantity + oi2.quantity) as weight 
                        from orders o1, orders o2, order_items oi1, order_items oi2
                        where datediff(o2.order_date, o1.order_date) < %s and
                            o2.order_date > o1.order_date and
                            o2.order_id = oi2.order_id and 
                            o1.order_id = oi1.order_id and
                            o1.order_id <> o2.order_id
                            and o1.store_id = %s  and o2.store_id = %s
                        group by o1.order_id, o2.order_id """


            cursor.execute(query, (num_giorni, id_store, id_store, ))

            for row in cursor:
                res.append(a.Arco(**row))

            cursor.close()
            cnx.close()

            return res


