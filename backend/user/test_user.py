from backend.user import UserApi
import fire

def testCheckOut():
    user_api = UserApi()

    rent_id = 0
    print(user_api.checkOut(rent_id))

def testGetOfficeOccupation():
    user_api = UserApi()

    id_office=0
    month=7
    print(user_api.getOfficeOccupation(id_office, month))

if __name__ == "__main__":
    fire.Fire()