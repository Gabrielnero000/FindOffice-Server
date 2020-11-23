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

        pre_update = f"SELECT * FROM offices WHERE officeId = {office_info['officeId']}"
        cursor.execute(pre_update)
        db_office_pre = cursor.fetchone()

        update = (
            f"UPDATE offices "
            f"SET ownerId = '{office_info['ownerId']}', "
            f"address = '{office_info['address']}', "
            f"district = '{office_info['district']}', "
            f"number = '{office_info['number']}', "
            f"extra = '{office_info['extra']}', "
            f"scoring = '{office_info['scoring']}', "
            f"nScore = '{office_info['nScore']}' "
            f"WHERE officeId = {office_info['officeId']}")

        cursor.execute(update)

        post_update = f"SELECT * FROM offices WHERE officeId = {office_info['officeId']}"
        cursor.execute(post_update)
        db_office_post = cursor.fetchone()

        if db_office_post is None:
            return {
                'success': False,
                'error': 'Office not found'
            }
        if db_office_pre == db_office_post:
            return {
                'success': False,
                'error': 'Office not modified'
            }
        return{
            'success': True,
            'office': db_office_post
        }

    def addOffice(self, office):
        cursor = self._db.getCursor()

        sql = "INSERT INTO offices (ownerId, address, district, number, extra, scoring, nScore) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (office['id_owner'], office['address'], office['district'],
                  office['number'], office['extra'], office['scoring'], office['nScore'])
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