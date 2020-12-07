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
    landmaster_api = LandmasterApi()

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
    landmaster_api.addOffice(office)

def testTop_score_office():
    landmaster_api = LandmasterApi()
    id_landmaster = 1
    # office = {
    #     'landmasterId': 1,
    #     'city': 'Tavares',
    #     'district': 'Paraiba',
    #     'address': 'Rua dos Ipes',
    #     'number': '50',
    #     'description': 'Lugar bonito',
    #     'daily_rate': 10.0,
    #     'capacity':20,
    #     'type': 'Residencial'
    # }
    # office2 = {
    #     'landmasterId': 0,
    #     'city': 'João Pessoa',
    #     'district': 'Paraiba',
    #     'address': 'Rua dos Ipes',
    #     'number': '50',
    #     'description': 'Lugar bonito',
    #     'daily_rate': 3.0,
    #     'capacity':20,
    #     'type': 'Residencial'
    # }

    # landmaster_api.addOffice(office)
    # landmaster_api.addOffice(office2)
    
    # office_info = {
    #     'officeId': 1,
    #     'landmasterId': 1,
    #     'city': 'joao pessoa',
    #     'district': 'mangabeira',
    #     'address': 'rua x',
    #     'number': 123,
    #     'description': 'desc',
    #     'daily_rate': 400.0,
    #     'capacity': 200,
    #     'scoring': 7,
    #     'nScore': 77,
    #     'type': 'business'
    # }

    # office_info2 = {
    #     'officeId': 2,
    #     'landmasterId': 1,
    #     'city': 'tavares',
    #     'district': 'mangabeira',
    #     'address': 'rua x',
    #     'number': 123,
    #     'description': 'desc',
    #     'daily_rate': 400.0,
    #     'capacity': 200,
    #     'scoring': 10,
    #     'nScore': 77,
    #     'type': 'business'
    # }

    # landmaster_api.modifyOffice(office_info)
    # landmaster_api.modifyOffice(office_info2)
    # print(landmaster_api.getOffices(id_landmaster))
    print(landmaster_api.top_score_office(id_landmaster))

def testGetMonthRents():
    landmaster_api = LandmasterApi()

    id_landmaster = 0
    print(landmaster_api.getMonthRents(id_landmaster))

def testGetMonthValue():
    landmaster_api = LandmasterApi()

    id_landmaster = 0
    print(landmaster_api.getMonthRents(id_landmaster))

if __name__ == "__main__":
    fire.Fire()