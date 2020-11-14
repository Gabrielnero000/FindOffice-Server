from backend.auth import AuthApi
from backend.tenant import TenantApi
from backend.user import UserApi
from flask import Flask, request, jsonify
import fire

app = Flask(__name__)

auth_api = AuthApi()
user_api = UserApi()
tenant_api = TenantApi()

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    return jsonify(auth_api.login(data['email'], data['password']))


@app.route('/auth/sign_up', methods=['POST'])
def sign_up():
    data = request.json
    return jsonify(auth_api.singUp(data['user']))

@app.route('/tenant/get_offices', methods=['POST'])
def get_offices():
    data = request.json
    return jsonify(tenant_api.getOffices(data['tenant_id']))

@app.route('/tenant/exclude_office', methods=['POST'])
def exclude_office():
    data = request.json
    return jsonify(tenant_api.excludeOffice(data['office_id']))

def launch(port=5804, debug=False):
    app.run(debug=debug, port=port, host='0.0.0.0', threaded=False)


if __name__ == "__main__":
    fire.Fire(launch)
