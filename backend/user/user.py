from backend.api import Api
from datetime import date


class UserApi(Api):
    def __init__(self):
        super().__init__()


    def checkOut(self, id_rent):
        cursor = self._db.getCursor()

        data_atual = date.today()

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


 