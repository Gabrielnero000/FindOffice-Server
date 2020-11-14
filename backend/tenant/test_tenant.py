from backend.tenant import TenantApi
import fire

def testGetOffices():
    tenant_api = TenantApi()

    tenant_id = 0
    print(tenant_api.getOffices(tenant_id))

def testexcludeOffice():
    tenant_api = TenantApi()

    office_id = 0
    print(tenant_api.excludeOffice(office_id))

if __name__ == "__main__":
    fire.Fire()