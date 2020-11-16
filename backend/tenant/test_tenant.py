from backend.tenant import TenantApi
import fire

def testGetOffices():
    tenant_api = TenantApi()

    tenant_id = 0
    print(tenant_api.getOffices(tenant_id))

def testAddOffice():
    tenant_api = TenantApi()

    office = {
        'id_owner': 1,
        'addres': 'João Pessoa, Bancarios, Rua dos Ipes',
        'district': 'Paraiba',
        'number': '50',
        'extra': 'lugar bonito',
        'scoring': 5,
        'nscore': 10
    }

    pp(tenant_api.addOffice(office))


if __name__ == "__main__":
    fire.Fire()