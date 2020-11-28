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

@app.route('/tenant/modify_office', methods=['POST'])
def modify_office():
    data = request.json
    return jsonify(tenant_api.modifyOffice(data['office']))

@app.route('/user/check_in', methods=['POST'])
def check_in():
    data = request.json
    return jsonify(user_api.checkIn(data['rent_id']))

@app.route('/user/check_out', methods=['POST'])
def check_out():
    data = request.json
    return jsonify(user_api.checkOut(data['rent_id']))

@app.route('/user/get_office_occupation', methods=['POST'])
def get_office_occupation():
    data = request.json
    return jsonify(user_api.getOfficeOccupation(data['office_id'], data['month']))

@app.route('/user/rent', methods=['POST'])
def rent():
    data = request.json
    return jsonify(user_api.rent(data['office_id'], data['user_id'], data['rent_days']))

@app.route('/user/get_all_offices', methods=['GET'])
def get_all_offices():
    data = request.json
    return jsonify(user_api.get_all_offices())
    
def launch(port=5804, debug=False):
    app.run(debug=debug, port=port, host='0.0.0.0', threaded=False)


if __name__ == "__main__":
    fire.Fire(launch)