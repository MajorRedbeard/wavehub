from flask import Blueprint, jsonify

ports = Blueprint('ports', __name__)

@ports.route('/ports/check/<int:port>', methods=['GET'])
def check_port(port):
    # Placeholder logic to check port availability
    return jsonify({"port": port, "status": "available"})
