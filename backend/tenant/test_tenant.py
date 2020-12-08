from backend.tenant import TenantApi
import fire
import datetime

def testCheckIn():
    user_api = TenantApi()

    rent_id = 3
    print(user_api.checkIn(rent_id))

def testCheckOut():
    user_api = TenantApi()

    rent_id = 1
    print(user_api.checkOut(rent_id))

def testGetOfficeOccupation():
    user_api = TenantApi()

    id_office=0
    month=7
    print(user_api.getOfficeOccupation(id_office, month))

def testRent():
    user_api = TenantApi()

    id_office = 4
    id_tenant = 2
    days = [datetime.datetime(2020,12,5), datetime.datetime(2020,12,6), datetime.datetime(2020,12,7)]
    print(user_api.rent(id_office, id_tenant, days))

def testGet_all_offices():
    user_api = TenantApi()

    #Quando puder adicionar imóveis testo novamente
    print(user_api.get_all_offices())

def testSearchOffices():
    user_api = TenantApi()

    filter = {
        'description': "",
        'city': None,
        'district': "",
        'capacity': 0,
        'min_price': 0.,
        'max_price': 999.,
        'available_now': True
    }
    print(user_api.searchOffices(filter))


def testGet_Rents():
    user_api = TenantApi()

    user_id = 0
    print(user_api.get_rents(user_id))    

def testScoreOffice():
    user_api = TenantApi()

    rent_id = 7
    score = 4
    print(user_api.scoreOffice(rent_id,score))


if __name__ == "__main__":
    fire.Fire()