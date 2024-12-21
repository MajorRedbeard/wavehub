import subprocess
from flask import Blueprint, jsonify, request
from ..config import SERVICES

services = Blueprint('services', __name__)

# Default list of common services and ports
COMMON_SERVICES = {
    "nginx": 80,
    "n8n": 5678,
    "uptime_kuma": 3000,
    "portainer": 9000,
    "grafana": 3001
}

@services.route('/discover', methods=['GET'])
def discover_services():
    found_services = []
    for name, port in COMMON_SERVICES.items():
        result = subprocess.run(
            ["ss", "-tuln"],
            stdout=subprocess.PIPE,
            text=True
        )
        if f":{port} " in result.stdout:
            found_services.append({"name": name, "port": port})
    return jsonify(found_services)

@services.route('/add', methods=['POST'])
def add_service():
    data = request.json
    name = data.get('name')
    port = data.get('port')
    SERVICES[name] = {"subdomain": name, "port": port}
    return jsonify({"message": f"Service '{name}' added successfully", "success": True})
