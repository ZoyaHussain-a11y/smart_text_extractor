from flask import Blueprint, request, jsonify
from utils.auth import generate_token, verify_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/token', methods=['POST'])
def generate_token_endpoint():
    """
    Generate a new JWT token
    
    Request:
    - No body required
    
    Response:
    {
        "token": "your-jwt-token-here",
        "expires_in": 86400  # seconds (1 day)
    }
    """
    try:
        token = generate_token()
        return jsonify({
            'token': token,
            'expires_in': 86400  # 1 day in seconds
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/api/auth/validate', methods=['GET'])
def validate_token():
    """
    Validate an existing JWT token
    
    Request:
    - Header: Authorization: Bearer <your-token>
    
    Response:
    {
        "valid": true/false,
        "message": "Token is valid/invalid"
    }
    """
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({
            'valid': False,
            'message': 'Missing Authorization header'
        }), 401
    
    token = token.replace('Bearer ', '')
    
    try:
        valid = verify_token(token)
        if valid:
            return jsonify({
                'valid': True,
                'message': 'Token is valid'
            })
        else:
            return jsonify({
                'valid': False,
                'message': 'Token is invalid or expired'
            }), 401
    except Exception as e:
        return jsonify({
            'valid': False,
            'message': str(e)
        }), 401
