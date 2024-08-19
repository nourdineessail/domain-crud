from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import json

app = Flask(__name__)

# Configure JWT
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Replace with a secret key
jwt = JWTManager(app)

# Load domains from JSON file
def load_domains():
    with open('domains.json', 'r') as f:
        return json.load(f)

# Save domains to JSON file
def save_domains(domains):
    with open('domains.json', 'w') as f:
        json.dump(domains, f, indent=4)

# Check if domain is in the whitelist
@app.route('/check-domain', methods=['GET'])
def check_domain():
    domain = request.args.get('domain')
    if not domain:
        return jsonify({"error": "Domain is required"}), 400

    domains = load_domains().get("domains", [])
    is_whitelisted = domain in domains
    return jsonify({"domain": domain, "is_whitelisted": is_whitelisted})

# Add domain to the whitelist (JWT required)
@app.route('/add-domain', methods=['POST'])
@jwt_required()
def add_domain():
    data = request.get_json()
    domain = data.get('domain')

    if not domain:
        return jsonify({"error": "Domain is required"}), 400

    domains_data = load_domains()
    domains = domains_data.get("domains", [])

    if domain in domains:
        return jsonify({"error": "Domain already exists"}), 400

    domains.append(domain)
    save_domains(domains_data)
    return jsonify({"message": f"Domain '{domain}' added successfully"}), 200

# Remove domain from the whitelist (JWT required)
@app.route('/remove-domain', methods=['DELETE'])
@jwt_required()
def remove_domain():
    data = request.get_json()
    domain = data.get('domain')

    if not domain:
        return jsonify({"error": "Domain is required"}), 400

    domains_data = load_domains()
    domains = domains_data.get("domains", [])

    if domain not in domains:
        return jsonify({"error": "Domain does not exist"}), 400

    domains.remove(domain)
    save_domains(domains_data)
    return jsonify({"message": f"Domain '{domain}' removed successfully"}), 200

# Get all whitelisted domains (JWT required)
@app.route('/get-domains', methods=['GET'])
@jwt_required()
def get_domains():
    domains_data = load_domains()
    return jsonify(domains_data), 200


if __name__ == '__main__':
    app.run(debug=True)
