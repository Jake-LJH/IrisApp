from model.DatabasePool import DatabasePool
import datetime

class IrisData:

    @classmethod
    def insertData(cls,sL,sW,pL,pW,result,timestamp):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql = "INSERT into iris_pred(sepal_len, sepal_w, petal_len, petal_w, result, timestamp) values(%s,%s,%s,%s,%s,%s)"  
             
            cursor.execute(sql,(sL, sW, pL, pW, result, timestamp))
            dbConn.commit()
            recordCount = cursor.rowcount
            print(cursor.lastrowid)
            return recordCount
        finally: 
            dbConn.close()
    
    @classmethod
    def getAllPred(cls):
        dbConn = DatabasePool.getConnection()
        cursor = dbConn.cursor(dictionary=True)

        sql = "select * from iris_pred"   
        cursor.execute(sql)
        data = cursor.fetchall()
        dbConn.close()

        return data

    @classmethod
    def deletePred(cls,id):
        dbConn = DatabasePool.getConnection()
        cursor = dbConn.cursor(dictionary=True)

        sql = "DELETE from iris_pred WHERE id=%s"   
        cursor.execute(sql,(id,))
        dbConn.commit()
        rows = cursor.rowcount
        dbConn.close()

        return rows
