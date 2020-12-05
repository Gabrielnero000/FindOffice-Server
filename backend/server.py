from backend.auth import AuthApi
from backend.tenant import TenantApi
from backend.landmaster import LandmasterApi
from flask import Flask, request, jsonify
import fire

app = Flask(__name__)

auth_api = AuthApi()
tenant_api = TenantApi()
landmaster_api = LandmasterApi()

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    return jsonify(auth_api.login(data['email'], data['password'], data['type']))


@app.route('/auth/sign_up', methods=['POST'])
def sign_up():
    data = request.json
    return jsonify(auth_api.signUp(data['user']))

@app.route('/landmaster/get_offices', methods=['POST'])
def get_offices():
    data = request.json
    return jsonify(landmaster_api.getOffices(data['tenant_id']))

@app.route('/landmaster/exclude_office', methods=['POST'])
def exclude_office():
    data = request.json
    return jsonify(landmaster_api.excludeOffice(data['office_id']))

@app.route('/landmaster/top_score_office', methods=['POST'])
def top_score_office():
    data = request.json
    return jsonify(landmaster_api.top_score_office(data['id_landmaster']))

@app.route('/landmaster/modify_office', methods=['POST'])
def modify_office():
    data = request.json
    return jsonify(landmaster_api.modifyOffice(data['office']))

@app.route('/tenant/check_in', methods=['POST'])
def check_in():
    data = request.json
    return jsonify(tenant_api.checkIn(data['rent_id']))

@app.route('/tenant/check_out', methods=['POST'])
def check_out():
    data = request.json
    return jsonify(tenant_api.checkOut(data['rent_id']))

@app.route('/tenant/get_office_occupation', methods=['POST'])
def get_office_occupation():
    data = request.json
    return jsonify(tenant_api.getOfficeOccupation(data['office_id'], data['month']))

@app.route('/tenant/rent', methods=['POST'])
def rent():
    data = request.json
    return jsonify(tenant_api.rent(data['office_id'], data['tenant_id'], data['rent_days']))

@app.route('/tenant/get_all_offices', methods=['GET'])
def get_all_offices():
    data = request.json
    return jsonify(tenant_api.get_all_offices())

@app.route('/tenant/search_offices', methods=['GET'])
def search_offices():
    data = request.json
    return jsonify(tenant_api.searchOffices(data['filter']))

def launch(port=5804, debug=False):
    app.run(debug=debug, port=port, host='0.0.0.0', threaded=False)


if __name__ == "__main__":
    fire.Fire(launch)