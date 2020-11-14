from backend.tenant import TenantApi
import fire

def testGetOffices():
    tenant_api = TenantApi()

    tenant_id = 0
    print(tenant_api.getOffices(tenant_id))

def testExclude_office():
    tenant_api = TenantApi()

    office_id = 0
    print(tenant_api.exclude_office(office_id))

if __name__ == "__main__":
    fire.Fire()