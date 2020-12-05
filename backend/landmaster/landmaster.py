from backend.api import Api

import datetime

class LandmasterApi(Api):
    def __init__(self):
        super().__init__()

    def getOffices(self, id_landmaster):
        cursor = self._db.getCursor()

        sql = f"SELECT * FROM offices WHERE landmasterId = '{id_landmaster}'"
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
            f"UPDATE offices SET "
            f"landmasterId = {office_info['landmasterId']}"
            f"city = '{office_info['city']}', "
            f"district = '{office_info['district']}', "
            f"address = '{office_info['address']}', "
            f"number = '{office_info['number']}', "
            f"description = '{office_info['description']}', "
            f"daily_rate = '{office_info['daily_rate']}', "
            f"capacity = '{office_info['capacity']}', "
            f"scoring = '{office_info['scoring']}', "
            f"nScore = '{office_info['nScore']}', "
            f"type = '{office_info['type']}' "
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

        sql = "INSERT INTO offices (landmasterId, city, district, address, number, description, daily_rate, capacity, scoring, nScore, type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (office['landmasterId'], office['city'], office['district'], office['address'],
                  office['number'], office['description'], office['daily_rate'], office['capacity'], 0, 0, office['type'])
        cursor.execute(sql, values)
        self._db.commit()

        query_sql = "SELECT * FROM offices WHERE officeId = last_insert_id()"
        cursor.execute(query_sql)
        db_office = cursor.fetchone()

        if db_office is None:
            return {
                'success': False,
                'error': 'Erro ao inserir'
            }

        return {
            'success': True,
            'office': db_office,
            'error': None
        }

    def getMonthRents(self, id_landmaster):
        cursor = self._db.getCursor()

        sql_offices = f"SELECT officeId FROM offices WHERE landmasterId = '{id_landmaster}'"
        cursor.execute(sql_offices)
        db_offices = cursor.fetchall()

        if len(db_offices) == 0:
            return{
                'success': False,
                'error': 'Could not find any office with this landmasterId'
            }

        month = datetime.date.today().month

        sql_rents = (
            f"SELECT * FROM rents WHERE officeId IN {*db_offices['officeId'],} "
            f"AND (MONTH(bookingStart) = '{month}' OR MONTH(bookingEnd) = '{month}') "
            f"ORDER BY bookingStart")
        cursor.execute(sql_rents)
        db_rents = cursor.fetchall()

        return {
            'success': True,
            'rents': db_rents
        }

    def getMonthValue(self, id_landmaster):
        cursor = self._db.getCursor()

        sql_offices = f"SELECT officeId, daily_rate FROM offices WHERE landmasterId = '{id_landmaster}' "
        cursor.execute(sql_offices)
        db_offices = cursor.fetchall()

        if len(db_offices) == 0:
            return{
                'success': False,
                'error': 'Could not find any office with this landmasterId'
            }

        month = datetime.date.today().month

        sql_rents = (
            f"SELECT officeId, bookingStart, bookingEnd FROM rents "
            f"WHERE officeId IN {*db_offices['officeId'],} "
            f"AND (MONTH(bookingStart) = '{month}' OR MONTH(bookingEnd) = '{month}')")
        cursor.execute(sql_rents)
        db_rents = cursor.fetchall()

        value = 0
        if len(db_rents) > 0:
            for officeId, start, end in zip(db_rents['officeId'], db_rents['bookingStart'],
                                            db_rents['bookingEnd']):
                occupied_days = [start + datetime.timedelta(days=x) for x in range((end-start).days+1)
                                if (start + datetime.timedelta(days=x)).month == month]
                index = db_offices['officeId'].index(officeId)
                value += len(occupied_days)*db_offices['daily_rate'][index]

        return {
            'success': True,
            'value': value
        }