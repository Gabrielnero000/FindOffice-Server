from backend.landmaster import LandmasterApi
import fire

def testGetOffices():
    tenant_api = LandmasterApi()

    landlord_id = 0
    print(tenant_api.getOffices(landlord_id))

def testexcludeOffice():
    tenant_api = LandmasterApi()

    office_id = 0
    print(tenant_api.excludeOffice(office_id))

def testModifyOffice():
    tenant_api = LandmasterApi()

    office_info = {
        'officeId': 0,
        'landmasterId': 0,
        'city': 'joao pessoa',
        'district': 'mangabeira',
        'address': 'rua x',
        'number': 123,
        'description': 'desc',
        'daily_rate': 400.0,
        'capacity': 200,
        'scoring': 7,
        'nScore': 77,
        'type': 'business'
    }
    print(tenant_api.modifyOffice(office_info))

def testAddOffice():
    tenant_api = LandmasterApi()

    office = {
        'landmasterId': 1,
        'city': 'JP',
        'district': 'bancarios',
        'address': 'Rua dos Ipes',
        'number': '50',
        'description': 'Lugar bonito',
        'daily_rate': 50.0,
        'capacity': 200,
        'type': 'Residencial'
    }
    print(tenant_api.addOffice(office))

if __name__ == "__main__":
    fire.Fire()