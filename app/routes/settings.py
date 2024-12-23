import os
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash

# File for storing settings
SETTINGS_FILE = "settings.json"

def get_settings():
    """Retrieve settings from the JSON file."""
    if not os.path.exists(SETTINGS_FILE):
        return {"server_domain": "wavehub.local"}
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(new_settings):
    """Save settings to the JSON file."""
    with open(SETTINGS_FILE, "w") as f:
        json.dump(new_settings, f)

# Blueprint for settings management
settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    """View and update settings."""
    current_settings = get_settings()

    if request.method == 'POST':
        # Update settings
        new_domain = request.form.get('server_domain')
        if not new_domain:
            flash("Domain cannot be empty.", "error")
        else:
            current_settings["server_domain"] = new_domain
            save_settings(current_settings)
            flash("Settings updated successfully.", "success")
            return redirect(url_for('settings.settings'))

    return render_template('settings.html', settings=current_settings)

# Template for the settings page
SETTINGS_TEMPLATE = """
{% extends 'base.html' %}
{% block content %}
<h2>Settings</h2>
<form method="POST">
    <label for="server_domain">Server Domain:</label>
    <input type="text" id="server_domain" name="server_domain" value="{{ settings.server_domain }}">
    <button type="submit">Save</button>
</form>

{% with messages = get_flashed_messages(with_categories=True) %}
    {% if messages %}
        <ul>
            {% for category, message in messages %}
                <li class="{{ category }}">{{ message }}</li>
            {% endfor %}
        </ul>
    {% endif %}
{% endwith %}
{% endblock %}
"""

def register_settings_template(app):
    """Register the settings template if not using an actual HTML file."""
    from flask import render_template_string

    @app.route('/settings', methods=['GET', 'POST'])
    def settings_inline():
        current_settings = get_settings()
        if request.method == 'POST':
            new_domain = request.form.get('server_domain')
            if not new_domain:
                flash("Domain cannot be empty.", "error")
            else:
                current_settings["server_domain"] = new_domain
                save_settings(current_settings)
                flash("Settings updated successfully.", "success")
                return redirect(url_for('settings_inline'))

        return render_template_string(SETTINGS_TEMPLATE, settings=current_settings)
