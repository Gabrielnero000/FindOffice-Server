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
        officeId_list = [d['officeId'] for d in db_offices]

        sql_rents = (
            f"SELECT * FROM rents WHERE officeId IN {*officeId_list,} "
            f"AND (MONTH(bookingStart) = '{month}' OR MONTH(bookingEnd) = '{month}') "
            f"ORDER BY bookingStart")
        cursor.execute(sql_rents)
        db_rents = cursor.fetchall()

        return {
            'success': True,
            'rents': db_rents
        }

    def top_score_office(self,id_landmaster):
        cursor = self._db.getCursor()

        sql = f"SELECT * FROM offices WHERE landmasterId = '{id_landmaster}' ORDER BY scoring/nScore DESC LIMIT 1"
        cursor.execute(sql)
        office = cursor.fetchall()

        if len(office) == 0:
            return{
                'success': False,
                'error': 'Could not find any office with this landmasterId'
            }

        return {
            'success': True,
            'office': office
        }

    def getTotalValue(self, id_landmaster):
        cursor = self._db.getCursor()

        sql_offices = f"SELECT officeId, daily_rate FROM offices WHERE landmasterId = '{id_landmaster}'"
        cursor.execute(sql_offices)
        db_offices = cursor.fetchall()

        if len(db_offices) == 0:
            return{
                'success': False,
                'error': 'Could not find any office with this landmasterId'
            }

        officeId_list = [d['officeId'] for d in db_offices]

        sql_rents = (
            f"SELECT officeId, bookingStart, bookingEnd FROM rents "
            f"WHERE officeId IN {*officeId_list,}")
        cursor.execute(sql_rents)
        db_rents = cursor.fetchall()

        month_average = 0
        daily_rate_list = [d['daily_rate'] for d in db_offices]
        if len(db_rents) > 0:
            for month in range (1,13):
                value = 0
                for d in db_rents:
                    occupied_days = [
                        d['bookingStart'] + datetime.timedelta(days=x)
                        for x in range((d['bookingEnd']-d['bookingStart']).days+1)
                                    if (d['bookingStart'] + datetime.timedelta(days=x)).month == month]
                    index = officeId_list.index(d['officeId'])
                    value += len(occupied_days)*daily_rate_list[index]
                month_average += value

        month_average /= 12

        return {
            'success': True,
            'month average': month_average
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
        officeId_list = [d['officeId'] for d in db_offices]

        sql_rents = (
            f"SELECT officeId, bookingStart, bookingEnd FROM rents "
            f"WHERE officeId IN {*officeId_list,} "
            f"AND (MONTH(bookingStart) = '{month}' OR MONTH(bookingEnd) = '{month}')")
        cursor.execute(sql_rents)
        db_rents = cursor.fetchall()

        value = 0
        daily_rate_list = [d['daily_rate'] for d in db_offices]
        if len(db_rents) > 0:
            for d in db_rents:
                occupied_days = [d['bookingStart'] + datetime.timedelta(days=x)
                                for x in range((d['bookingEnd']-d['bookingStart']).days+1)
                                if (d['bookingStart'] + datetime.timedelta(days=x)).month == month]
                index = officeId_list.index(d['officeId'])
                value += len(occupied_days)*daily_rate_list[index]

        return {
            'success': True,
            'value': value
        }

    def topRentsOffice(self, id_landmaster):
        cursor = self._db.getCursor()
        sql_offices = f"SELECT officeId FROM offices WHERE landmasterId = '{id_landmaster}'"
        cursor.execute(sql_offices)
        db_offices = cursor.fetchall()

        if len(db_offices) == 0:
            return{
                'success': False,
                'error': 'Could not find any office with this landmasterId'
            }

        officeId_list = [d['officeId'] for d in db_offices]

        sql_rents = (
            f"SELECT officeId, bookingStart, bookingEnd "
            f"FROM rents WHERE officeId IN {*officeId_list,}")
        cursor.execute(sql_rents)
        db_rents = cursor.fetchall()

        rents_per_officeId = [0]*len(db_offices)
        if len(db_rents) > 0:
            for d in db_rents:
                occupied_days = [d['bookingStart'] + datetime.timedelta(days=x)
                                for x in range((d['bookingEnd']-d['bookingStart']).days+1)]
                index = officeId_list.index(d['officeId'])
                rents_per_officeId[index] += len(occupied_days)

        max_rents = max(rents_per_officeId)
        indices = [i for i, x in enumerate(rents_per_officeId) if x == max_rents]

        sql = f"SELECT * FROM offices WHERE officeId IN {*[officeId_list[i] for i in indices],}"
        print(sql)
        cursor.execute(sql)
        office = cursor.fetchall()

        return {
            'success': True,
            'office': office,
            'value': max_rents
        }

    def get_top_value_office(self, id_landmaster):
        cursor = self._db.getCursor()

        sql_offices = f"SELECT officeId, daily_rate FROM offices WHERE landmasterId = '{id_landmaster}'"
        cursor.execute(sql_offices)
        db_offices = cursor.fetchall()

        if len(db_offices) == 0:
            return{
                'success': False,
                'error': 'Could not find any office with this landmasterId'
            }

        officeId_list = [d['officeId'] for d in db_offices]

        sql_rents = (
            f"SELECT officeId, bookingStart, bookingEnd "
            f"FROM rents WHERE officeId IN {*officeId_list,}")
        cursor.execute(sql_rents)
        db_rents = cursor.fetchall()

        daily_rate_list = [d['daily_rate'] for d in db_offices]
        value_per_officeId = [0]*len(db_offices)
        if len(db_rents) > 0:
            for d in db_rents:
                occupied_days = [d['bookingStart'] + datetime.timedelta(days=x)
                                for x in range((d['bookingEnd']-d['bookingStart']).days+1)]
                index = officeId_list.index(d['officeId'])
                value_per_officeId[index] += len(occupied_days)*daily_rate_list[index]

        max_rents = max(value_per_officeId)
        indices = [i for i, x in enumerate(value_per_officeId) if x == max_rents]

        sql = f"SELECT * FROM offices WHERE officeId IN {*[officeId_list[i] for i in indices],}"
        cursor.execute(sql)
        office = cursor.fetchall()

        return {
            'success': True,
            'office': office,
        }