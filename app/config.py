
# Central configuration file

BASE_DOMAIN = "wavehub.local"
SERVICES = {
    "nginx": {"subdomain": "nginx", "port": 80},
    "n8n": {"subdomain": "n8n", "port": 5678},
    "uptime_kuma": {"subdomain": "uptimekuma", "port": 3000},
}
