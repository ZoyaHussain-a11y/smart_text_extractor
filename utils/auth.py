from functools import wraps
from flask import request, jsonify
import os
from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_token():
    """Generate a JWT token with expiration"""
    secret_key = os.getenv('JWT_SECRET')
    if not secret_key:
        raise ValueError("JWT_SECRET not found in environment variables")
        
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1),  # Token expires in 1 day
        'iat': datetime.utcnow(),
        'sub': 'user'
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')

def verify_token(token: str) -> bool:
    """Verify JWT token"""
    secret_key = os.getenv('JWT_SECRET')
    if not secret_key:
        raise ValueError("JWT_SECRET not found in environment variables")
        
    try:
        jwt.decode(token, secret_key, algorithms=['HS256'])
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False

def require_token(f):
    """Decorator to require JWT token for endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({
                'error': 'Missing Authorization header',
                'documentation': 'Include Authorization header with Bearer token'
            }), 401
            
        # Extract token from 'Bearer <token>' format
        token = token.replace('Bearer ', '')
        
        if not verify_token(token):
            return jsonify({
                'error': 'Invalid or expired token',
                'documentation': 'Token has expired or is invalid'
            }), 401
            
        return f(*args, **kwargs)
    return decorated_function

def generate_and_save_token():
    """Generate and save a new JWT token"""
    token = generate_token()
    return token
