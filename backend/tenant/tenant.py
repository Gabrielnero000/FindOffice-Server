from backend.api import Api

class TenantApi(Api):
    def __init__(self):
        super().__init__()

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
        db_office = cursor.fetchone()

        if db_office is None:
            return {
                'success': False,
                'error': 'Office not found'
            }
        return{
            'success': True,
            'office': db_office
        }