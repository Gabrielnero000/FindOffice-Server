from backend.user import UserApi
import fire

def testGetOfficeOccupation():
    user_api = UserApi()

    id_rent=0
    month=7
    print(user_api.getOfficeOccupation(id_rent, month))

if __name__ == "__main__":
    fire.Fire()