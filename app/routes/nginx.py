import os
import subprocess
from flask import Blueprint, request, jsonify
from ..config import BASE_DOMAIN, SERVICES

nginx = Blueprint('nginx', __name__)

NGINX_AVAILABLE = "/etc/nginx/sites-available"
CONFIG_FILE = "/etc/nginx/sites-available/wavehub"

def list_existing_subdomains():
    subdomains = []
    for filename in os.listdir(NGINX_AVAILABLE):
        if filename.endswith(".conf") or filename in ["default"]:
            path = os.path.join(NGINX_AVAILABLE, filename)
            with open(path, "r") as f:
                for line in f:
                    if "server_name" in line:
                        domain = line.strip().split()[1].strip(";")
                        subdomains.append(domain)
    return subdomains

@nginx.route('/nginx/suggest', methods=['GET'])
def suggest_nginx_changes():
    existing = list_existing_subdomains()
    suggested = []
    for service, details in SERVICES.items():
        expected_subdomain = f"{details['subdomain']}.{BASE_DOMAIN}"
        if expected_subdomain not in existing:
            suggested.append({
                "subdomain": expected_subdomain,
                "port": details["port"],
                "service": service
            })
    return jsonify(suggested)

@nginx.route('/nginx/apply', methods=['POST'])
def apply_nginx_changes():
    changes = request.json.get("changes", [])
    changes_applied = []

    for change in changes:
        subdomain = change["subdomain"]
        port = change["port"]
        service = change["service"]
        
        # Update Nginx configuration
        with open(CONFIG_FILE, "a") as config_file:
            config_file.write(f"""
server {{
    listen 80;
    server_name {subdomain};

    location / {{
        proxy_pass http://127.0.0.1:{port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }}
}}
""")
        changes_applied.append(subdomain)

    # Validate and reload Nginx
    validation_result = subprocess.run(["nginx", "-t"], stdout=subprocess.PIPE, text=True)
    if validation_result.returncode != 0:
        return jsonify({
            "error": "Nginx configuration validation failed",
            "details": validation_result.stdout
        }), 400

    subprocess.run(["systemctl", "reload", "nginx"])
    return jsonify({"message": "Changes applied successfully", "applied": changes_applied})
