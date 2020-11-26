from backend.user import UserApi
import fire

def testCheckOut():
    user_api = UserApi()

    rent_id = 0
    print(user_api.checkOut(rent_id))


if __name__ == "__main__":
    fire.Fire()