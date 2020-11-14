from backend.api import Api

class TenantApi(Api):
    def __init__(self):
        super().__init__()

    def getOffices(self, id_tenant):
        cursor = self._db.getCursor()

        sql = f"SELECT * FROM offices WHERE ownerId = '{id_tenant}'"
        cursor.execute(sql)
        
        return {
            'success': True,
            'offices': cursor.fetchall()
        }

    def exclude_office(self):
        print("teste!")

    def addOffices(self, id_owner, address, district, number, extra, scoring, nScore):
        cursor = self._db.getCursor()

        sql = "INSERT INTO offices (ownerId, address, district, number, extra, scoring, nScore) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (offices['id_owner'], offices['address'], offices['district'],
                  offices['number'], offices['extra'], offices['scoring'], offices['nScore'])
        cursor.execute(sql, values)
        self._db.commit()

        query_sql = "SELECT * FROM offices WHERE officeId = last_insert_id()"
        cursor.execute(query_sql)
        db_office = cursor.fetchone()

        return {
            'success':True,
            'office': db_office,
            'error':None
        }