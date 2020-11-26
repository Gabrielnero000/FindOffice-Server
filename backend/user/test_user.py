from backend.user import UserApi
import fire
import datetime

def testGetOfficeOccupation():
    user_api = UserApi()

    id_office=0
    month=7
    print(user_api.getOfficeOccupation(id_office, month))

def testRent():
    user_api = UserApi()

    id_office = 0
    id_user = 0
    days = [datetime.datetime(2020,10,20), datetime.datetime(2020,10,21), datetime.datetime(2020,10,22)]
    print(user_api.rent(id_office, id_user, days))

if __name__ == "__main__":
    fire.Fire()