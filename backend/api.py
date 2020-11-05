from backend.tenant import TenantApi
from backend.user import UserApi
from flask import Flask, request, jsonify
import fire

app = Flask(__name__)

user_api = UserApi()
tenant_api = TenantApi()

@app.route('/user/get_all_offices', methods=['GET'])
def get_all_offices():
    return jsonify(user_api.getAllOffices())

@app.route('/tenant/add_office', methods=['POST'])
def add_office():
    return jsonify(tenant_api.addOffice())

def launch(port=5804, debug=False):
    app.run(debug=debug, port=port, host='0.0.0.0', threaded=False)

if __name__ == "__main__":
    fire.Fire(launch)