from backend.api import Api

import datetime

class TenantApi(Api):
    def __init__(self, today):
        super().__init__(today)

    def checkIn(self, id_rent):
        cursor = self._db.getCursor()

        current_date = self._today

        preCheckIn = f"SELECT bookingStart FROM rents WHERE rentId = '{id_rent}'"
        cursor.execute(preCheckIn)
        db_PreCheckIn = cursor.fetchone()

        if abs((current_date - db_PreCheckIn['bookingStart']).days) <= 0:

            update = (
            f"UPDATE rents "
            f"SET checkIn = '{current_date}' "
            f"WHERE rentId = '{id_rent}'")
            cursor.execute(update)

            validation = f"SELECT checkIn FROM rents WHERE rentId = '{id_rent}'"
            cursor.execute(validation)
            db_validation = cursor.fetchone()

            if (current_date - db_validation['checkIn']).days > 0:
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

        current_date = self._today

        preCheckOut = f"SELECT checkIn FROM rents WHERE rentId = '{id_rent}'"
        cursor.execute(preCheckOut)
        db_preCheckOut = cursor.fetchone()

        if db_preCheckOut is None:
            return {
            'success': False,
            'error': 'You have to check-in first.'
        }
        else:
            update = (
            f"UPDATE rents "
            f"SET checkOut = '{current_date}' "
            f"WHERE rentId = '{id_rent}'")
            cursor.execute(update)

            validation = f"SELECT checkOut FROM rents WHERE rentId = '{id_rent}'"
            cursor.execute(validation)
            db_validation = cursor.fetchone()

            if abs((current_date - db_validation['checkOut']).days) > 0:
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
            f"AND (MONTH(bookingStart) = '{month}' OR MONTH(bookingEnd) = '{month}') "
            f"ORDER BY bookingStart")
        cursor.execute(sql)
        db_rents = cursor.fetchall()

        occupied_days = []
        if len(db_rents) > 0:
            for d in db_rents:
                occupied_days.extend([(d['bookingStart'] + datetime.timedelta(days=x)).isoformat()
                                    for x in range((d['bookingEnd']-d['bookingStart']).days + 1)
                                    if (d['bookingStart'] + datetime.timedelta(days=x)).month == month])

        return {
            'success': True,
            'days': occupied_days
        }

    def rent(self, id_office, id_tenant, rent_days):
        cursor = self._db.getCursor()
        
        start = datetime.datetime.strptime(rent_days[0], '%Y-%m-%d')
        end = datetime.datetime.strptime(rent_days[-1], '%Y-%m-%d')

        insert = (
            f"INSERT INTO rents (officeId, tenantId, bookingStart, bookingEnd) "
            f"VALUES ({id_office}, {id_tenant}, '{start}', '{end}')")
        cursor.execute(insert)
        self._db.commit()

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

        if 'description' in filter and type(filter['description']) == str:
            sql += conjunction(sql)
            sql += f"description LIKE '%{filter['description']}%' "

        if 'type' in filter and (filter['type'] == 'business' or filter['type'] == 'residential'):
            sql += conjunction(sql)
            sql += f"type LIKE '%{filter['type']}%' "

        if 'city' in filter and type(filter['city']) == str:
            sql += conjunction(sql)
            sql += f"city LIKE '%{filter['city']}%' "

        if 'district' in filter and type(filter['district']) == str:
            sql += conjunction(sql)
            sql += f"district LIKE '%{filter['district']}%' "

        if 'capacity' in filter and type(filter['capacity']) == int and filter['capacity'] >= 0:
            sql += conjunction(sql)
            sql += f"capacity >= {filter['capacity']} "

        if ('min_price' in filter and type(filter['min_price']) == float and filter['min_price'] >= 0
            and 'max_price' in filter and type(filter['max_price']) == float
            and filter['max_price'] >= filter['min_price']):
            sql += conjunction(sql)
            sql += f"(daily_rate BETWEEN {filter['min_price']} AND {filter['max_price']}) "

        if 'order_by' in filter and (filter['order_by'] == 'score' or filter['order_by'] == 'price'):
            sql += (
                f"ORDER BY (CASE WHEN '{filter['order_by']}' = 'price' THEN daily_rate END) ASC, "
                f"(CASE WHEN '{filter['order_by']}' = 'score' THEN scoring END) DESC")

        cursor.execute(sql)
        db_offices = cursor.fetchall()

        if 'available_now' in filter and filter['available_now'] == True and len(db_offices) > 0:
            for d in db_offices:
                occupied_days = self.getOfficeOccupation(d['officeId'], self._today.month)
                if self._today.isoformat() in occupied_days['days']:
                    db_offices.remove(d)

        return {
            'success': True,
            'offices': db_offices
        }


    def get_rents(self, id_tenant):
        cursor = self._db.getCursor()

        sql = f"SELECT * FROM rents WHERE tenantId = '{id_tenant}'"
        cursor.execute(sql)
        my_rents = cursor.fetchall()

        no_checkIn = []
        no_checkOut = []
        no_scoring = []
        past_rents = []

        if(my_rents is None):

            return{
                'success': False,
                'warning': 'User not found or user with no past rents'
            }

        else:

            for rent in my_rents:

                if(rent['checkIn'] is None):
                    no_checkIn.append(rent)

                elif(rent['checkOut'] is None):
                    no_checkOut.append(rent)

                elif(rent['scoring'] is None):
                    no_scoring.append(rent)

                else:
                    past_rents.append(rent)


        rents = {
            'no_checkIn': no_checkIn,
            'no_checkOut': no_checkOut,
            'no_scoring': no_scoring,
            'past_rents': past_rents
        }

        return{
            'success': True,
            'rents': rents
        }

    def scoreOffice(self, id_rent, score):
        cursor = self._db.getCursor()

        select_office = f"SELECT * FROM rents WHERE rentId = {id_rent}"
        cursor.execute (select_office)
        db_office = cursor.fetchone()
        update_rent = (
            f"UPDATE rents SET "
            f"scoring = {score} "
            f"WHERE rentId = {id_rent}")
        cursor.execute (update_rent)
        self._db.commit()

        select_scores = f"SELECT * FROM offices WHERE officeId = {db_office['officeId']}"
        cursor.execute (select_scores)
        scr = cursor.fetchone()

        update_office = (
            f"UPDATE offices SET "
            f"scoring = {scr['scoring']} + {score}, "
            f"nScore = '{scr['nScore']}' + '{1}'"
            f"WHERE officeId = {db_office['officeId']}")
        cursor.execute (update_office)
        self._db.commit()

        return{
            'success': True,
            'office': scr,
            'rent': db_office
        }




