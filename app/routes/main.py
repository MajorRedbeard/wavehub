
from flask import Blueprint, render_template
from ..config import BASE_DOMAIN, SERVICES

main = Blueprint('main', __name__)

@main.route('/')
def dashboard():
    # Placeholder: Simulating service statuses
    for service in SERVICES:
        SERVICES[service]["status"] = "running" if service != "n8n" else "stopped"

    return render_template('dashboard.html', services=SERVICES, base_domain=BASE_DOMAIN)
