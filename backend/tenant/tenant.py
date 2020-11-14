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

    def exclude_office(self, id_office):
        cursor = self._db.getCursor()

        sql = f"DELETE FROM offices WHERE officeId  = '{id_office}'"
        cursor.execute(sql)

        sql = f"SELECT * FROM offices WHERE officeId = '{id_office}'"
        cursor.execute(sql)

        db_office = cursor.fetchone()

        if db_office is not None:
            return {
                'success': False,
                'error': 'Office not deleted'
            }
        return{
            'sucess': True
        }
