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

    def excludeOffice(self, id_office):
        cursor = self._db.getCursor()

        sql = f"DELETE FROM offices WHERE officeId  = '{id_office}'"
        cursor.execute(sql)

        sql = f"SELECT * FROM offices WHERE officeId = '{id_office}'"
        cursor.execute(sql)

        db_office = cursor.fetchone()

        if db_office is not None:
            return {
                'success': False,
                'error': 'Office not excluded'
            }
        return{
            'sucess': True
        }

    def modifyOffice(self, office_info):
        cursor = self._db.getCursor()

        sql = (
            f"UPDATE offices "
            f"SET ownerId = '{office_info['ownerId']}', "
            f"address = '{office_info['address']}', "
            f"district = '{office_info['district']}', "
            f"number = '{office_info['number']}', "
            f"extra = '{office_info['extra']}', "
            f"scoring = '{office_info['scoring']}', "
            f"nScore = '{office_info['nScore']}' "
            f"WHERE officeId = {office_info['officeId']}")

        cursor.execute(sql)

        return_sql = f"SELECT * FROM offices WHERE officeId = {office_info['officeId']}"

        cursor.execute(return_sql)
        db_office = cursor.fetchone()

        if db_office is None:
            return {
                'success': False,
                'error': 'Office not found'
            }
        if db_office != tuple(office_info.values()):
            return {
                'success': False,
                'error': 'Office not modified'
            }
        return{
            'success': True,
            'office': db_office
        }
