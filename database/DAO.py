from database.DB_connect import DBConnect
from model.airport import Airport
from model.arco import Arco


class DAO():

    @staticmethod
    def getAirposts(numMinimo):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT  a.*, count(distinct f.AIRLINE_ID) as numeroCompagne
                    from airports a , flights f 
                    where (a.ID =f.ORIGIN_AIRPORT_ID or a.ID =f.DESTINATION_AIRPORT_ID) 
                    group by a.ID
                    having count(distinct f.AIRLINE_ID)>=%s """

        cursor.execute(query, (numMinimo,))

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result



    @staticmethod
    def getEdges(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT f.ORIGIN_AIRPORT_ID as aereoporto1, f.DESTINATION_AIRPORT_ID as aereoporto2, count(*) as numVoli
        FROM flights f
        group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID  
        order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID 
        """

        cursor.execute(query )

        for row in cursor:
            if row["aereoporto1"] in idMap and row["aereoporto2"] in idMap: #CONTROLLO SE ESISTONO DEI NODI CON in!!!
                result.append(Arco(idMap[row["aereoporto1"]], idMap[row["aereoporto2"]], row["numVoli"]))

        cursor.close()
        conn.close()
        return result
