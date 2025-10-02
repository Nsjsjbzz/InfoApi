from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/bin-check/<bin_code>', methods=['GET'])
def bin_check(bin_code):
    """Get raw BIN check response"""
    try:
        url = f"https://bins.antipublic.cc/bins/{bin_code}"
        response = requests.get(url)
        return response.text, response.status_code, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cc-generator', methods=['GET'])
def cc_generator():
    """Get raw CC generator response"""
    try:
        bin_code = request.args.get('bin', '')
        count = request.args.get('count', '10')
        
        url = f"https://drlabapis.onrender.com/api/ccgenerator?bin={bin_code}&count={count}"
        response = requests.get(url)
        return response.text, response.status_code, {'Content-Type': 'text/plain'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/fake-address', methods=['GET'])
def fake_address():
    """Get raw fake address response"""
    try:
        country_code = request.args.get('country', 'US')
        url = f"https://randomuser.me/api/?nat={country_code}"
        response = requests.get(url)
        return response.text, response.status_code, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/all-raw', methods=['GET'])
def all_raw():
    """Get all 3 raw responses in one call"""
    try:
        bin_code = request.args.get('bin', '')
        count = request.args.get('count', '10')
        country_code = request.args.get('country', 'US')
        
        # BIN Check
        bin_url = f"https://bins.antipublic.cc/bins/{bin_code}"
        bin_response = requests.get(bin_url)
        
        # CC Generator
        cc_url = f"https://drlabapis.onrender.com/api/ccgenerator?bin={bin_code}&count={count}"
        cc_response = requests.get(cc_url)
        
        # Fake Address
        address_url = f"https://randomuser.me/api/?nat={country_code}"
        address_response = requests.get(address_url)
        
        return jsonify({
            'bin_check': bin_response.json(),
            'cc_generator': cc_response.text,
            'fake_address': address_response.json()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    """Home page with API documentation"""
    docs = {
        'message': 'Raw API Proxy Service',
        'endpoints': {
            '/api/bin-check/<bin_code>': {
                'method': 'GET',
                'description': 'Raw BIN check response from antipublic.cc'
            },
            '/api/cc-generator': {
                'method': 'GET', 
                'parameters': {
                    'bin': 'BIN code (required)',
                    'count': 'Number of cards (optional, default: 10)'
                },
                'description': 'Raw CC generator response from drlabapis'
            },
            '/api/fake-address': {
                'method': 'GET',
                'parameters': {
                    'country': 'Country code (optional, default: US)'
                },
                'description': 'Raw fake address response from randomuser.me'
            },
            '/api/all-raw': {
                'method': 'GET',
                'parameters': {
                    'bin': 'BIN code (required)',
                    'count': 'Number of cards (optional, default: 10)',
                    'country': 'Country code (optional, default: US)'
                },
                'description': 'Get all 3 raw responses in one call'
            }
        },
        'example_usage': {
            'bin_check': '/api/bin-check/484783',
            'cc_generator': '/api/cc-generator?bin=544422&count=5',
            'fake_address': '/api/fake-address?country=us',
            'all_raw': '/api/all-raw?bin=544422&count=5&country=us'
        }
    }
    return jsonify(docs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)