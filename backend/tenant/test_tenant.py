from backend.tenant import TenantApi
import fire

def testModifyOffice():
    tenant_api = TenantApi()

    office_info = {
        'officeId': 0,
        'ownerId': 0,
        'address': 'rua',
        'district': 'dist',
        'number': '123',
        'extra': 'oi',
        'scoring': 7,
        'nScore': 77
    }
    print(tenant_api.modifyOffice(office_info))

if __name__ == "__main__":
    fire.Fire()