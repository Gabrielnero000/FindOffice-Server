from backend.auth import AuthApi
from backend.utils import pp
import fire

def testLogin():
    auth_api = AuthApi()

    email = 'gabriel@email.com'
    password = 'fake'

    pp(auth_api.login(email, password))


def testSignUp():
    auth_api = AuthApi()

    user = {
        'name': 'Gabriel',
        'email': 'gabriel@email.com',
        'password': 'fake',
        'type': 'landlord'
    }

    pp(auth_api.signUp(user))


if __name__ == "__main__":
    fire.Fire()