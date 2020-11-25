from backend.user import UserApi
import fire

def testGetOfficeOccupation():
    user_api = UserApi()

    id_office=0
    month=7
    print(user_api.getOfficeOccupation(id_office, month))

if __name__ == "__main__":
    fire.Fire()