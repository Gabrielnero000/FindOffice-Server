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
        'landlordId': 0,
        'address': 'rua',
        'district': 'dist',
        'number': '123',
        'description': 'desc',
        'scoring': 7,
        'nScore': 77,
        'daily_rate': 4.0,
        'type': 'escritorio'
    }
    print(tenant_api.modifyOffice(office_info))

def testAddOffice():
    tenant_api = LandmasterApi()

    office = {
        'id_landlord': 1,
        'addres': 'João Pessoa, Bancarios, Rua dos Ipes',
        'district': 'Paraiba',
        'number': '50',
        'description': 'Lugar bonito',
        'daily_rate': 5.0,
        'type': 'Residencial'
    }
    print(tenant_api.addOffice(office))

if __name__ == "__main__":
    fire.Fire()