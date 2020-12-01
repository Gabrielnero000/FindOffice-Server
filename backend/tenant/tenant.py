from backend.api import Api

import datetime
from calendar import monthrange


class TenantApi(Api):
    def __init__(self):
        super().__init__()

    def checkIn(self, id_rent):
        cursor = self._db.getCursor()

        current_date = datetime.date.today()

        preCheckIn = f"SELECT bookingStart FROM rents WHERE rentId = '{id_rent}'"
        cursor.execute(preCheckIn)
        db_PreCheckIn = cursor.fetchone()

        if db_PreCheckIn == current_date:

            update = (
            f"UPDATE rents"
            f"SET checkIn = '{current_date}'"
            f"WHERE rentId = '{id_rent}'")
            cursor.execute(update)

            validation = f"SELECT checkIn FROM rents WHERE rentId = '{id_rent}'"
            cursor.execute(validation)
            db_validation = cursor.fetchone()

            if db_validation != current_date:
                return {
                    'success': False,
                    'error': 'Unable to checkin'
                }

            return {
                'success': True
            }

        return {
                'success': False,
                'error': 'You can only check-in on the date of your booking.'
        }

    def checkOut(self, id_rent):
        cursor = self._db.getCursor()

        current_date = datetime.date.today()

        preCheckOut = f"SELECT checkIn FROM rents WHERE rentId = '{id_rent}'"
        cursor.execute(preCheckOut)
        db_preCheckOut = cursor.fetchone()

        if db_preCheckOut is None:
            return{
            'success': False,
            'error': 'You have to check-in first.'
            }

        else:
            update = (
            f"UPDATE rents"
            f"SET checkOut = '{current_date}'"
            f"WHERE rentId = '{id_rent}'")
            cursor.execute(update)

            validation = f"SELECT checkOut FROM rents WHERE rentId = '{id_rent}'"
            cursor.execute(validation)
            db_validation = cursor.fetchone()

            if db_validation != current_date:
                return {
                    'success': False,
                    'error': 'Unable to checkout'
                }

            return {
                    'success': True
            }


    def getOfficeOccupation(self, id_office, month):
        cursor = self._db.getCursor()

        sql = (
            f"SELECT bookingStart, bookingEnd FROM rents "
            f"WHERE officeId = '{id_office}' "
            f"AND (MONTH(bookingStart) = '{month}' OR MONTH(bookingEnd) = '{month}')")
        cursor.execute(sql)
        db_rents = cursor.fetchall()

        if len(db_rents) == 0:
            return {
                'success': True,
                'message': "All days are vacant in this month"
            }

        occupied_days = []
        for start, end in zip(db_rents['bookingStart'], db_rents['bookingEnd']):
            if start.month < month:
                occupied_days.extend(range(1, end.day+1))
            elif end.month > month:
                occupied_days.extend(range(start.day, monthrange(start.year, start.month)[1]+1))
            else:
                occupied_days.extend(range(start.day, end.day+1))

        return {
            'success': True,
            'days': occupied_days
        }

    def rent(self, id_office, id_tenant, rent_days):
        cursor = self._db.getCursor()

        insert = (
            f"INSERT INTO rents (officeId, tenantId, bookingStart, bookingEnd)"
            f"VALUES ('{id_office}', '{id_tenant}', '{rent_days[0]}', '{rent_days[-1]}')")
        cursor.execute(insert)

        select = f"SELECT * FROM rents WHERE rentId = LAST_INSERT_ID()"
        cursor.execute(select)
        db_rent = cursor.fetchone()

        return {
            'success': True,
            'rent': db_rent
        }

    def get_all_offices(self):
        cursor = self._db.getCursor()
        sql = "SELECT * FROM offices ORDER BY scoring/nScore DESC LIMIT 10"
        cursor.execute(sql)

        return {
            'success': True,
            'offices': cursor.fetchall()
        }

    def searchOffices(self, filter):
        cursor = self._db.getCursor()

        def conjunction(sql_string):
            if sql_string == "SELECT * FROM offices ":
                conj = "WHERE "
            else:
                conj = "AND "

            return conj

        sql = "SELECT * FROM offices "

        if type(filter['description']) == str:
            sql += conjunction(sql)
            sql += f"description LIKE '%{filter['description']}%' "

        if filter['type'] == 'business' or filter['type'] == 'residential':
            sql += conjunction(sql)
            sql += f"type LIKE '%{filter['type']}%' "

        if type(filter['city']) == str:
            sql += conjunction(sql)
            sql += f"city LIKE '%{filter['city']}%' "

        if type(filter['district']) == str:
            sql += conjunction(sql)
            sql += f"district LIKE '%{filter['district']}%' "

        if type(filter['capacity']) == int and filter['capacity'] >= 0:
            sql += conjunction(sql)
            sql += f"capacity >= {filter['capacity']} "

        if (type(filter['min_price']) == float and filter['min_price'] >= 0 and
            type(filter['max_price']) == float and filter['max_price'] >= filter['min_price']):
            sql += conjunction(sql)
            sql += f"(daily_rate BETWEEN {filter['min_price']} AND {filter['max_price']}) "

        if filter['order_by'] == 'score' or filter['order_by'] == 'price':
            sql += (
                f"ORDER BY (CASE WHEN '{filter['order_by']}' = 'price' THEN daily_rate END) ASC, "
                f"(CASE WHEN '{filter['order_by']}' = 'score' THEN scoring END) DESC")

        cursor.execute(sql)
        db_offices = cursor.fetchall()

        if filter['available_now'] == True and len(db_offices) > 0:
            for office_id in db_offices['officeId']:
                occupied_days = self.getOfficeOccupation(office_id, datetime.date.today().month)
                if datetime.date.today().day in occupied_days['days']:
                    index = db_offices['officeId'].index(office_id)
                    for column in db_offices.values():
                        column.pop(index)

        return {
            'success': True,
            'offices': db_offices
        }
