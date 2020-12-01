from backend.tenant import TenantApi
import fire
import datetime

def testCheckIn():
    user_api = TenantApi()

    rent_id = 0
    print(user_api.checkIn(rent_id))

def testCheckOut():
    user_api = TenantApi()

    rent_id = 0
    print(user_api.checkOut(rent_id))

def testGetOfficeOccupation():
    user_api = TenantApi()

    id_office=0
    month=7
    print(user_api.getOfficeOccupation(id_office, month))

def testRent():
    user_api = TenantApi()

    id_office = 0
    id_tenant = 0
    days = [datetime.datetime(2020,10,20), datetime.datetime(2020,10,21), datetime.datetime(2020,10,22)]
    print(user_api.rent(id_office, id_tenant, days))

def testGet_all_offices():
    user_api = TenantApi()

    #Quando puder adicionar imóveis testo novamente
    print(user_api.get_all_offices())

def testSearchOffices():
    user_api = TenantApi()

    filter = {
        'description': "",
        'type': "business",
        'city': "",
        'district': "",
        'capacity': 0,
        'min_price': 0,
        'max_price': 9999,
        'order_by': 'price',
        'available_now': True
    }
    print(user_api.searchOffices(filter))

if __name__ == "__main__":
    fire.Fire()