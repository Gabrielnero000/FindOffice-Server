from backend.api import Api

import datetime
from calendar import monthrange


class UserApi(Api):
    def __init__(self):
        super().__init__()

    def checkOut(self, id_rent):
        cursor = self._db.getCursor()

        data_atual = datetime.date.today()

        sql = f"SELECT * FROM rents WHERE rentId = '{id_rent}'"

        cursor.execute(sql)

        update = ( 
        f"UPDATE rents"
        f"SET checkOut = '{data_atual}'"
        f"WHERE rentId = '{id_rent}'")

        cursor.execute(update)

        valida = f"SELECT checkOut FROM rents WHERE rentId = '{id_rent}'"

        cursor.execute(valida)

        if valida != data_atual:
            return {
                'success': False,
                'error': 'Unable to checkout '
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
        # remove dias duplicados
        occupied_days = list(dict.fromkeys(occupied_days))

        return {
            'success': True,
            'days': occupied_days
        }
