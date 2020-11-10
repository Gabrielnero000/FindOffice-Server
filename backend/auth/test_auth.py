from backend.auth import AuthApi
from backend.utils import pp
import fire

def testLogin():
    auth_api = AuthApi()

    email = 'gabriel@email.com'
    password = 'fake'

    pp(auth_api.login(email, password))


def testSingUp():
    auth_api = AuthApi()

    user = {
        'name': 'Gabriel',
        'email': 'gabriel@email.com',
        'password': 'fake',
        'legalPerson': 0,
        'cpf': '09954817417',
        'cnpj': None,
        'isTenant': 0
    }

    pp(auth_api.singUp(user))


if __name__ == "__main__":
    fire.Fire()